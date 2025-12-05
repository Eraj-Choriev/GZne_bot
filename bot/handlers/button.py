"""
This module handles all button presses from the user.
"""
import logging
from telegram import Update, InlineKeyboardButton
from telegram.ext import ContextTypes

from ..state import USER_DATA, get_user_lang
from ..localization import get_locale
from .language import handle_language_selection, cmd_language
from .navigation import (
    handle_info, handle_category, handle_product, back_to_category,
    back_to_product
)
from .purchase import (
    handle_buy, handle_payment, handle_copy_requisites, handle_i_paid,
    handle_confirm_cancel, handle_cancel_order_final, handle_decline_cancel
)
from .receipt import (
    handle_send_receipt, handle_upload_another_receipt,
    handle_admin_approval, handle_admin_rejection
)
from .start import send_main_menu
from .support import cmd_support
from .errors import error_handler


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Enhanced button handler with improved UX and visual hierarchy.
    Applies Ogilvy's clarity and Jobs' simplicity principles.
    """
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = query.data

    logging.info("Button press from user %s: %s", user_id, data)

    # Initialize user data if needed
    if user_id not in USER_DATA:
        USER_DATA[user_id] = {}

    lang = get_user_lang(user_id)
    L = get_locale(lang)

    try:
        # ============================================
        # ROUTING LOGIC - Organized by User Journey
        # ============================================

        # 1. LANGUAGE SETTINGS
        if data in ('lang_ru', 'lang_tj'):
            await handle_language_selection(update, context)

        elif data == 'change_lang':
            await _handle_language_menu(query, context)

        # 2. NAVIGATION - HOME
        elif data in ('cmd_start', 'back_main', 'main_menu'):
            USER_DATA[user_id] = {
                'language': lang,
                'state': None,
                'auth': USER_DATA[user_id].get('auth', {})
            }
            await send_main_menu(query.message, context, lang)

        # 3. INFORMATION & SUPPORT
        elif data == 'cat_info':
            await handle_info(update, context)

        elif data == 'cat_support':
            await _handle_support(query, context)

        # 4. CATEGORY BROWSING
        elif data.startswith('cat_'):
            await handle_category(update, context)

        elif data == 'back_category':
            await back_to_category(update, context)

        # 5. PRODUCT DETAILS
        elif data.startswith('prod_'):
            await handle_product(update, context)

        elif data == 'back_product':
            await back_to_product(update, context)

        # 6. PURCHASE FLOW
        elif data.startswith('buy_'):
            await handle_buy(update, context)

        elif data.startswith('pay_'):
            await handle_payment(update, context)

        elif data == 'copy_requisites':
            await handle_copy_requisites(update, context)

        elif data == 'i_paid':
            await handle_i_paid(update, context)

        elif data == 'confirm_cancel':
            await handle_confirm_cancel(update, context)

        elif data == 'cancel_order_confirmed':
            await handle_cancel_order_final(update, context)

        elif data == 'cancel_order_declined':
            await handle_decline_cancel(update, context)

        # 7. RECEIPT & ADMIN
        elif data == 'send_receipt':
            await handle_send_receipt(update, context)

        elif data == 'upload_another_receipt':
            await handle_upload_another_receipt(update, context)

        elif data.startswith('admin_approve_'):
            await handle_admin_approval(update, context)

        elif data.startswith('admin_reject_'):
            await handle_admin_rejection(update, context)

        else:
            # Unknown callback - log and show friendly message
            logging.getLogger(__name__).warning(
                "Unknown callback data: %s from user %s", data, user_id
            )
            await query.answer(
                L.get('error_unknown_action', '❌ Unknown action'),
                show_alert=True
            )

    except Exception as e:
        logging.getLogger(__name__).error(
            "Error in button_handler (data: %s, user: %s): %s",
            data, user_id, e,
            exc_info=True
        )
        await error_handler(update, context)


# ============================================
# ENHANCED UI HELPER FUNCTIONS
# ============================================

async def _handle_language_menu(query, context):
    """Show language selection with enhanced UI"""
    fake_update = type('Update', (object,), {
        'message': query.message,
        'effective_user': query.from_user
    })()
    await cmd_language(fake_update, context)


async def _handle_support(query, context):
    """Show support menu with enhanced UI"""
    fake_update = type('Update', (object,), {
        'message': query.message,
        'effective_user': query.from_user
    })()
    await cmd_support(fake_update, context)