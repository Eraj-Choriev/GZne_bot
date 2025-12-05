from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from .localization import get_locale


def get_lang_keyboard() -> InlineKeyboardMarkup:
    """Returns the beautiful language selection inline keyboard with Tajik first."""
    keyboard = [
        [InlineKeyboardButton("🇹🇯 Тоҷикӣ", callback_data="lang_tj")],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_back_button(lang: str, to: str) -> InlineKeyboardButton:
    """Returns a standardized 'Back' button."""
    return InlineKeyboardButton(get_locale(lang)['back_btn'], callback_data=f"back_{to}")


def get_main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Returns the main menu inline keyboard."""
    L = get_locale(lang)
    keyboard = [
        [
            InlineKeyboardButton("🔄 Сменить язык", callback_data="change_lang"),
            InlineKeyboardButton("💬 Поддержка", callback_data="cat_support"),
        ],
        [InlineKeyboardButton(L['cat_info_btn'], callback_data="cat_info")],
        [InlineKeyboardButton(L['cat_games_btn'], callback_data="cat_games")],
        [InlineKeyboardButton(L['cat_currency_btn'], callback_data="cat_currency")],
        [InlineKeyboardButton(L['cat_mobile_btn'], callback_data="cat_mobile")],
        [InlineKeyboardButton(L['cat_services_btn'], callback_data="cat_services")],
        [InlineKeyboardButton(L['cat_software_btn'], callback_data="cat_software")],
    ]
    return InlineKeyboardMarkup(keyboard)