import asyncio
import logging
from datetime import timedelta
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from ..config import Config
from ..state import USER_DATA, get_user_lang
from ..localization import get_locale
from ..keyboards import get_back_button
from ..data import find_product, generate_order_id
from ..payments import get_payment_method_details

from .start import send_main_menu

# Import database functions
try:
    from ..models import create_order, update_order_status, track_event
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False

logger = logging.getLogger(__name__)

# --- Helper Functions ---

def get_payment_keyboard(lang: str, admin_url: str) -> InlineKeyboardMarkup:
    """Builds the inline keyboard for the payment page."""
    L = get_locale(lang)
    keyboard = [
        [
            InlineKeyboardButton(L['copy_requisites_btn'], callback_data='copy_requisites'),
            InlineKeyboardButton(L['i_paid_btn'], callback_data='i_paid'),
        ],
        [
            InlineKeyboardButton(L['payment_issues_btn'], url=admin_url),
            InlineKeyboardButton(L['cancel_order_btn'], callback_data='confirm_cancel'),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def schedule_order_jobs(context: ContextTypes.DEFAULT_TYPE, user_id: int, order_id: str, lang: str):
    """Schedules reminder and timeout jobs for an order."""
    L = get_locale(lang)
    
    # Schedule reminder
    reminder_job = context.job_queue.run_once(
        order_reminder,
        timedelta(minutes=15),
        data={'user_id': user_id, 'order_id': order_id, 'lang': lang},
        name=f"reminder_{user_id}_{order_id}"
    )

    # Schedule timeout
    timeout_job = context.job_queue.run_once(
        order_timeout,
        timedelta(minutes=30),
        data={'user_id': user_id, 'order_id': order_id, 'lang': lang},
        name=f"timeout_{user_id}_{order_id}"
    )

    # Store job names to be able to cancel them later
    USER_DATA[user_id]['jobs'] = [f"reminder_{user_id}_{order_id}", f"timeout_{user_id}_{order_id}"]

def remove_scheduled_jobs(context: ContextTypes.DEFAULT_TYPE, user_id: int):
    """Removes scheduled jobs for a user."""
    if 'jobs' in USER_DATA.get(user_id, {}):
        for job_id in USER_DATA[user_id]['jobs']:
            jobs = context.job_queue.get_jobs_by_name(job_id)
            for job in jobs:
                job.schedule_removal()
        del USER_DATA[user_id]['jobs']

# --- Job Functions (for timer) ---

async def order_reminder(context: ContextTypes.DEFAULT_TYPE):
    """Sends a reminder to the user that their order is about to expire."""
    job = context.job
    user_id = job.data['user_id']
    order_id = job.data['order_id']
    lang = job.data['lang']
    L = get_locale(lang)

    await context.bot.send_message(
        chat_id=user_id,
        text=L['order_reminder'].format(order_id=order_id)
    )

async def order_timeout(context: ContextTypes.DEFAULT_TYPE):
    """Cancels an order automatically if the user doesn't pay in time."""
    job = context.job
    user_id = job.data['user_id']
    order_id = job.data['order_id']
    lang = job.data['lang']
    L = get_locale(lang)

    if USER_DATA.get(user_id, {}).get('order_id') == order_id:
        USER_DATA[user_id]['state'] = None
        USER_DATA[user_id]['order_id'] = None
        # Also remove the payment page message if possible
        if 'payment_message_id' in USER_DATA[user_id]:
            try:
                await context.bot.edit_message_text(
                    chat_id=user_id,
                    message_id=USER_DATA[user_id]['payment_message_id'],
                    text=L['order_timed_out'].format(order_id=order_id),
                    reply_markup=None
                )
            except Exception:
                pass # Message might have been deleted
        
        await context.bot.send_message(
            chat_id=user_id,
            text=L['order_timed_out'].format(order_id=order_id)
        )
        await send_main_menu(context.bot, user_id, lang)


# --- Core Handlers ---

async def handle_buy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays the payment method selection screen."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_lang(user_id)
    L = get_locale(lang)

    # 2x2 grid for payment methods
    keyboard = [
        [
            InlineKeyboardButton(L['pay_dc_btn'], callback_data='pay_dc'),
            InlineKeyboardButton(L['pay_eskhata_btn'], callback_data='pay_eskhata'),
        ],
        [
            InlineKeyboardButton(L['pay_alif_btn'], callback_data='pay_alif'),
            InlineKeyboardButton(L['pay_visa_btn'], callback_data='pay_visa'),
        ],
        [get_back_button(lang, 'product')],
    ]
    await query.message.edit_text(
        L['choose_payment'], 
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generates and displays the detailed payment page for the selected method."""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    lang = get_user_lang(user_id)
    L = get_locale(lang)
    cfg = Config.load()
    admin_username = cfg.admin_username or '@gzone_admin_ctrl'
    admin_url = f"https://t.me/{admin_username.lstrip('@')}"

    payment_method_key = query.data
    order_id = generate_order_id()
    
    if 'current_product' not in USER_DATA[user_id]:
        await query.answer(L.get('session_expired', "Session expired. Please start over."), show_alert=True)
        await send_main_menu(query.message, context, lang)
        return

    product = find_product(lang, USER_DATA[user_id]['current_product'])
    if not product:
        raise ValueError("Product not found in session")
    
    price = product['price']
    method_name, account_details = get_payment_method_details(lang, payment_method_key)
    currency = "TJS" if payment_method_key in ['pay_dc', 'pay_eskhata', 'pay_alif', 'pay_visa'] else "RUB"

    # Store order info
    USER_DATA[user_id].update({
        'payment_method': payment_method_key,
        'state': 'awaiting_payment',
        'order_id': order_id,
        'price': price,
        'currency': currency,
        'account_details': account_details,
        'method_name': method_name,
    })

    # Save order to database
    if DB_AVAILABLE:
        try:
            # Get product category (from current_product ID)
            product_category = USER_DATA[user_id].get('current_category', 'unknown')

            create_order(
                telegram_id=user_id,
                order_id=order_id,
                product_id=USER_DATA[user_id]['current_product'],
                product_name=product.get('name', 'Unknown Product'),
                product_category=product_category,
                price_tjs=price if currency == 'TJS' else 0,
                price_usd=price if currency == 'USD' else price / 10.6  # Convert TJS to USD approx
            )
            logger.info(f"✅ Order {order_id} saved to database for user {user_id}")

            # Track purchase attempt event
            track_event(user_id, 'purchase_initiated', f'Product: {product.get("name")}, Order: {order_id}')
        except Exception as e:
            logger.error(f"❌ Failed to save order to database: {e}")
            # Continue anyway - order info is still in USER_DATA

    # Build the payment message
    # Calculate old price
    old_price = price * 2
    
    full_text = L['payment_page_template'].format(
        method_name=method_name,
        old_price=f"{old_price:.2f}",
        price=f"{price:.2f}",
        currency=currency,
        user_id=user_id,
        account_details=account_details
    )

    # Send Message
    try:
        await query.message.delete() # Clean up previous message
    except Exception:
        pass # Message might already be deleted

    # Try to send the payment message
    try:
        sent_message = await context.bot.send_message(
            chat_id=user_id,
            text=full_text,
            reply_markup=get_payment_keyboard(lang, admin_url),
            parse_mode=ParseMode.HTML,
        )
    except Exception as e:
        # Only show error if message sending actually failed
        import logging
        logging.error(f"Failed to send payment page: {e}")
        await context.bot.send_message(
            chat_id=user_id,
            text="❌ Ошибка при отправке страницы оплаты. Попробуйте еще раз."
        )
        await send_main_menu(context.bot, user_id, lang)
        return

    # Store message info and schedule jobs (after successful message send)
    try:
        USER_DATA[user_id]['payment_message_id'] = sent_message.message_id
        await schedule_order_jobs(context, user_id, order_id, lang)
    except Exception as e:
        # Log error but don't show error to user since payment page was sent successfully
        import logging
        logging.error(f"Failed to schedule jobs for order {order_id}: {e}")


# --- Button Callback Handlers ---

async def handle_copy_requisites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Copies payment requisites to clipboard (sends them as a message)."""
    query = update.callback_query
    user_id = query.from_user.id
    lang = get_user_lang(user_id)
    L = get_locale(lang)

    user_info = USER_DATA.get(user_id, {})
    if user_info.get('state') == 'awaiting_payment':
        await query.answer(L['requisites_copied_alert'], show_alert=True)
        await context.bot.send_message(user_id, f"<code>{user_info['account_details']}</code>", parse_mode=ParseMode.HTML)
    else:
        await query.answer()


async def handle_i_paid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Transitions user to receipt upload flow with manager contact."""
    query = update.callback_query
    user_id = query.from_user.id
    lang = get_user_lang(user_id)
    L = get_locale(lang)
    cfg = Config.load()
    admin_username = cfg.admin_username or '@gzone_admin_ctrl'
    admin_url = f"https://t.me/{admin_username.lstrip('@')}"

    if USER_DATA.get(user_id, {}).get('state') == 'awaiting_payment':
        # Clean up timer jobs
        remove_scheduled_jobs(context, user_id)

        # Set state to await receipt upload
        USER_DATA[user_id]['state'] = 'awaiting_receipt'
        await query.answer()

        # Delete the payment message to keep chat clean
        try:
            await query.message.delete()
        except Exception:
            pass

        # Show receipt request with manager contact and cancel button
        keyboard = [
            [InlineKeyboardButton(L['contact_manager_link_btn'], url=admin_url)],
            [InlineKeyboardButton(L['cancel_order_btn'], callback_data='cancel_order_confirmed')]
        ]

        await context.bot.send_message(
            user_id,
            L['receipt_request_template'],
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )
    else:
        await query.answer()


async def handle_confirm_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Asks for confirmation before cancelling an order."""
    query = update.callback_query
    lang = get_user_lang(query.from_user.id)
    L = get_locale(lang)
    
    keyboard = [
        [
            InlineKeyboardButton(L['confirm_cancel_order_btn'], callback_data='cancel_order_confirmed'),
            InlineKeyboardButton(L['decline_cancel_order_btn'], callback_data='cancel_order_declined'),
        ]
    ]
    await query.answer()
    await query.message.edit_text(
        L['cancel_confirmation_text'],
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_cancel_order_final(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Performs the final order cancellation."""
    query = update.callback_query
    user_id = query.from_user.id
    lang = get_user_lang(user_id)
    L = get_locale(lang)

    # Update order status in database
    if DB_AVAILABLE and USER_DATA.get(user_id, {}).get('order_id'):
        try:
            order_id = USER_DATA[user_id]['order_id']
            update_order_status(order_id, 'cancelled', 'Cancelled by user')
            logger.info(f"✅ Order {order_id} cancelled in database")

            # Track cancellation event
            track_event(user_id, 'order_cancelled', f'Order: {order_id}')
        except Exception as e:
            logger.error(f"❌ Failed to update order status: {e}")

    # Clean up user state
    remove_scheduled_jobs(context, user_id)
    USER_DATA[user_id]['state'] = None
    USER_DATA[user_id]['order_id'] = None

    await query.answer()
    await query.message.edit_text(L['order_cancelled'])
    await send_main_menu(context.bot, user_id, lang)

async def handle_decline_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Returns to the payment screen after declining cancellation."""
    # This is tricky because we have two messages now.
    # We can just re-send the instructions message with the keyboard.
    query = update.callback_query
    user_id = query.from_user.id
    lang = get_user_lang(user_id)
    L = get_locale(lang)
    cfg = Config.load()
    admin_username = cfg.admin_username or '@gzone_admin_ctrl'
    admin_url = f"https://t.me/{admin_username.lstrip('@')}"

    timer_line = L['payment_page_timer'].format(time_left="...") # We lost the exact time, need to recalculate or just show placeholder
    instructions_title = L['payment_page_important_instructions']
    instructions = "\n".join([
        L['payment_page_instruction_1'],
        L['payment_page_instruction_2'],
        L['payment_page_instruction_3'],
    ])
    instructions_text = (
        f"\n\n"
        f"{instructions_title}\n"
        f"{instructions}\n\n"
        f"{timer_line}"
    )
    await query.answer()
    await query.message.edit_text(
        instructions_text,
        reply_markup=get_payment_keyboard(lang, admin_url),
        parse_mode=ParseMode.HTML,
    )