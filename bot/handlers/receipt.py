from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from ..config import Config
from ..state import USER_DATA, get_user_lang
from ..localization import get_locale
from ..data import find_product, generate_product_key
from ..handlers.purchase import remove_scheduled_jobs
from .start import send_main_menu

# --- Receipt Handling Flow ---

async def receipt_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the initial upload of a receipt image."""
    user_id = update.message.from_user.id
    if USER_DATA.get(user_id, {}).get('state') != 'awaiting_receipt':
        return

    lang = get_user_lang(user_id)
    L = get_locale(lang)
    photo = update.message.photo[-1] # Get the highest resolution photo

    # Store file_id for later
    USER_DATA[user_id]['receipt_file_id'] = photo.file_id
    USER_DATA[user_id]['state'] = 'awaiting_receipt_confirmation'

    keyboard = [
        [
            InlineKeyboardButton(L['send_receipt_btn'], callback_data='send_receipt'),
            InlineKeyboardButton(L['upload_another_receipt_btn'], callback_data='upload_another_receipt'),
        ]
    ]
    
    await update.message.reply_photo(
    photo=photo.file_id,
    caption=f"<b>{L['receipt_preview_title']}</b>\n\n{L['receipt_preview_prompt']}",
    reply_markup=InlineKeyboardMarkup(keyboard),
    parse_mode=ParseMode.HTML,
)

async def handle_send_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Forwards the confirmed receipt to the admin for verification."""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    lang = get_user_lang(user_id)
    L = get_locale(lang)
    cfg = Config.load()

    if USER_DATA.get(user_id, {}).get('state') != 'awaiting_receipt_confirmation':
        return

    # Clean up timer jobs
    remove_scheduled_jobs(context, user_id)

    # Notify user
    await query.message.edit_caption(caption=L['receipt_pending'])

    # Prepare data for admin
    user_info = USER_DATA[user_id]
    admin_notification_text = L['admin_receipt_notification'].format(
        order_id=user_info.get('order_id', 'N/A'),
        user_mention=query.from_user.mention_html(),
        product_name=find_product(lang, user_info.get('current_product', '')).get('name', 'N/A'),
        price=user_info.get('price', 'N/A'),
        currency=user_info.get('currency', ''),
        method_name=user_info.get('method_name', 'N/A')
    )

    admin_keyboard = [
        [
            InlineKeyboardButton(L['admin_approve_btn'], callback_data=f"admin_approve_{user_id}_{user_info['order_id']}"),
            InlineKeyboardButton(L['admin_reject_btn'], callback_data=f"admin_reject_{user_id}_{user_info['order_id']}"),
        ]
    ]

    # Send to admin
    if cfg.admin_id:
        await context.bot.send_photo(
            chat_id=cfg.admin_id,
            photo=user_info['receipt_file_id'],
            caption=admin_notification_text,
            reply_markup=InlineKeyboardMarkup(admin_keyboard),
            parse_mode=ParseMode.HTML
        )
    
    USER_DATA[user_id]['state'] = 'pending_review'


async def handle_upload_another_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Allows the user to cancel the current receipt and upload a new one."""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    lang = get_user_lang(user_id)
    L = get_locale(lang)

    if USER_DATA.get(user_id, {}).get('state') == 'awaiting_receipt_confirmation':
        USER_DATA[user_id]['state'] = 'awaiting_receipt'
        await query.message.delete()
        await context.bot.send_message(user_id, L['send_receipt_prompt'])


# --- Admin Actions ---

async def handle_admin_approval(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the admin's approval of a payment."""
    query = update.callback_query
    await query.answer("✅ Approved")
    
    _, target_user_id, order_id = query.data.split('_')
    target_user_id = int(target_user_id)
    
    lang = get_user_lang(target_user_id)
    L = get_locale(lang)

    # Check if the order is still valid
    if USER_DATA.get(target_user_id, {}).get('order_id') != order_id:
        await query.message.edit_caption(caption=query.message.caption + "\n\n---\nProcessed (Order Expired or Changed)")
        return

    product_id = USER_DATA[target_user_id].get('current_product')
    product = find_product(lang, product_id)
    product_name = product.get('name', 'N/A') if product else 'N/A'
    key = generate_product_key()

    success_message = f"**{L['order_success_title']}**\n\n{L['order_success'].format(order_id=order_id, product_name=product_name, key=key)}"
    
    await context.bot.send_message(target_user_id, success_message, parse_mode=ParseMode.MARKDOWN_V2)
    
    # Clean up admin message
    await query.message.edit_caption(caption=query.message.caption + f"\n\n---\n✅ Approved by {query.from_user.mention_html()}")

    # Clean up user state
    USER_DATA[target_user_id] = {'language': lang} # Reset state
    await send_main_menu(context.bot, target_user_id, lang)


async def handle_admin_rejection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the admin's rejection of a payment."""
    query = update.callback_query
    await query.answer("❌ Rejected", show_alert=True)

    _, target_user_id, order_id = query.data.split('_')
    target_user_id = int(target_user_id)
    
    lang = get_user_lang(target_user_id)
    L = get_locale(lang)

    if USER_DATA.get(target_user_id, {}).get('order_id') != order_id:
        await query.message.edit_caption(caption=query.message.caption + "\n\n---\nProcessed (Order Expired or Changed)")
        return

    rejection_message = f"**{L['order_rejected_title']}**\n\n{L['order_rejected'].format(order_id=order_id)}"
    
    await context.bot.send_message(target_user_id, rejection_message, parse_mode=ParseMode.MARKDOWN_V2)

    # Clean up admin message
    await query.message.edit_caption(caption=query.message.caption + f"\n\n---\n❌ Rejected by {query.from_user.mention_html()}")

    # Reset user state but keep them in the payment flow to try again?
    # For now, let's just reset them to the main menu.
    USER_DATA[target_user_id] = {'language': lang}
    await send_main_menu(context.bot, target_user_id, lang)


# --- Fallbacks ---

async def invalid_receipt_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles non-photo messages when awaiting a receipt."""
    user_id = update.message.from_user.id
    if USER_DATA.get(user_id, {}).get('state') in ['awaiting_receipt', 'awaiting_receipt_confirmation']:
        lang = get_user_lang(user_id)
        await update.message.reply_text(get_locale(lang)['receipt_invalid_type'])
