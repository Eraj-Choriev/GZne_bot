import logging
from telegram import Update, Message, Bot
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from ..state import USER_DATA, get_user_lang
from ..localization import get_locale
from ..keyboards import get_main_menu_keyboard, get_lang_keyboard


async def send_main_menu(message_or_bot, context_or_user_id, lang: str, is_new_message: bool = False) -> None:
    """
    Send main menu to user. Can be called in two ways:
    1. send_main_menu(message, context, lang, is_new_message)
    2. send_main_menu(bot, user_id, lang)
    """
    L = get_locale(lang)
    text = L['main_menu']
    keyboard = get_main_menu_keyboard(lang)

    # Check if called with bot and user_id (2nd signature)
    if isinstance(message_or_bot, Bot):
        bot = message_or_bot
        user_id = context_or_user_id
        logging.info(f"send_main_menu called for user {user_id}")
        await bot.send_message(chat_id=user_id, text=text, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
    else:
        # Called with message and context (1st signature)
        message = message_or_bot
        logging.info(f"send_main_menu called for user {message.chat.id}")
        try:
            if is_new_message:
                await message.reply_text(text, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
            else:
                await message.edit_text(text, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
        except Exception:
            if not is_new_message:
                await message.reply_text(text, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

    # Check if user is new (no language set)
    existing_lang = USER_DATA.get(user_id, {}).get('language')

    if not existing_lang:
        # New user - show beautiful language selection screen
        welcome_text = (
           
            "🇹🇯 Лутфан, забонро интихоб кунед\n"
            "🇷🇺 Пожалуйста, выберите язык\n\n"
           
        )
        await update.message.reply_text(
            welcome_text,
            reply_markup=get_lang_keyboard(),
            parse_mode='HTML'
        )
    else:
        # Returning user - show main menu directly
        USER_DATA.setdefault(user_id, {})['language'] = existing_lang
        await send_main_menu(update.message, context, existing_lang, is_new_message=True)


async def cmd_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    lang = get_user_lang(user_id) or 'ru'
    USER_DATA.setdefault(user_id, {}).setdefault('language', lang)
    await send_main_menu(update.message, context, lang, is_new_message=True)