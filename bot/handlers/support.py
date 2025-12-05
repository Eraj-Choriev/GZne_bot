from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from ..config import Config


async def cmd_support(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    cfg = Config.load()
    admin = cfg.admin_username or '@gzone_admin_ctrl'
    if admin.startswith('@'):
        url = f"https://t.me/{admin[1:]}"
        await update.message.reply_text(
            f"Связаться с менеджером: {admin}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Написать менеджеру', url=url)]])
        )
    else:
        await update.message.reply_text(f"Связаться с менеджером: {admin}")
