import logging
from telegram import Update
from telegram.ext import ContextTypes

from ..state import get_user_lang
from ..localization import get_locale
from .start import send_main_menu

logger = logging.getLogger(__name__)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a generic message to the user."""
    logger.error("Exception while handling an update:", exc_info=context.error)
    try:
        if isinstance(update, Update) and update.effective_user:
            user_id = update.effective_user.id
            lang = get_user_lang(user_id)
            L = get_locale(lang)

            # Send error message
            try:
                await context.bot.send_message(chat_id=user_id, text=L['error_generic'])
            except Exception as send_error:
                logger.error(f"Failed to send error message: {send_error}")
                # Fallback to simple message without formatting
                await context.bot.send_message(
                    chat_id=user_id,
                    text="❌ Произошла ошибка. Возвращаемся в главное меню..."
                )

            # Try to recover by showing the main menu
            try:
                await send_main_menu(context.bot, user_id, lang)
            except Exception as menu_error:
                logger.error(f"Failed to show main menu: {menu_error}")
    except Exception as e:
        logger.error(f"Exception in error_handler: {e}", exc_info=True)