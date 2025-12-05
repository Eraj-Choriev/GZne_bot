from telegram import Update
from telegram.ext import ContextTypes

from ..state import USER_DATA
from ..localization import get_locale
from ..keyboards import get_lang_keyboard
from .start import send_main_menu


async def cmd_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for the /language command."""
    L_ru = get_locale('ru')
    L_tj = get_locale('tj')
    await update.message.reply_text(
        f"{L_ru.get('choose_language', 'Выберите язык:')}\n\n{L_tj.get('choose_language',)}",
        reply_markup=get_lang_keyboard(),
    )


async def handle_language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the language selection from the inline keyboard."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    lang = 'ru' if data == 'lang_ru' else 'tj'
    USER_DATA.setdefault(user_id, {})['language'] = lang

    # After language selection, always reset state and show the main menu.
    USER_DATA[user_id]['state'] = None
    await send_main_menu(query.message, context, lang)
