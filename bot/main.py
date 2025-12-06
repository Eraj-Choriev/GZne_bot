import logging
from telegram import Update, BotCommand
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from telegram.request import HTTPXRequest

from .config import Config
from .localization import load_locales, get_locale
from .state import get_user_lang
from .handlers import (
    start,
    language,
    support,
    button,
    receipt,
    text,
    errors
)

# Import database and logging setup
try:
    from .models import init_db
    from .logger import setup_logging
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    print("⚠️  Database modules not available. Running without DB support.")

logger = logging.getLogger(__name__)


def init_app():
    """Initialize the bot application."""
    # Setup logging (production-ready or fallback to basic)
    if DB_AVAILABLE:
        try:
            setup_logging()
            logger.info("✅ Production logging initialized")
        except Exception as e:
            logging.basicConfig(
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                level=logging.INFO
            )
            logger.warning(f"⚠️  Fallback to basic logging: {e}")
    else:
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.INFO
        )

    # Initialize database
    if DB_AVAILABLE:
        try:
            init_db()
            logger.info("✅ Database initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize database: {e}")
            logger.warning("⚠️  Bot will continue without database support")

    # Load locales and config
    load_locales()
    logger.info("✅ Locales loaded")

    cfg = Config.load()
    logger.info(f"✅ Config loaded for admin: {cfg.admin_username}")

    async def _post_init(app):
        try:
            await app.bot.set_my_commands([
                BotCommand('start', '🚀 Запустить или перезапустить бота'),
                BotCommand('menu', '🏠 Показать главное меню'),
                BotCommand('language', '🔄 Сменить язык'),
                BotCommand('support', '💬 Связаться с поддержкой'),
            ], language_code='ru')
        except Exception as e:
            logger.warning(f"set_my_commands skipped due to network error: {e}")

    request = HTTPXRequest(
        connect_timeout=30.0,
        read_timeout=60.0,
        write_timeout=60.0,
        pool_timeout=30.0,
    )

    app = ApplicationBuilder().token(cfg.bot_token).request(request).post_init(_post_init).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start.start))
    app.add_handler(CommandHandler("menu", start.cmd_menu))
    app.add_handler(CommandHandler("language", language.cmd_language))
    app.add_handler(CommandHandler("support", support.cmd_support))

    # Register callback query handler
    app.add_handler(CallbackQueryHandler(button.button_handler))

    # Register message handlers
    app.add_handler(MessageHandler(filters.PHOTO, receipt.receipt_handler))
    app.add_handler(MessageHandler(filters.Document.ALL | filters.VIDEO | filters.AUDIO | filters.VOICE | filters.Sticker.ALL, receipt.invalid_receipt_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text.main_text_router))

    # Register error handler
    app.add_error_handler(errors.error_handler)

    return app


def run() -> None:
    """Run the bot."""
    app = init_app()
    logger.info("=" * 60)
    logger.info("🚀 GZne Bot started successfully!")
    logger.info("=" * 60)
    logger.info("📊 Database: %s", "Enabled ✅" if DB_AVAILABLE else "Disabled ⚠️")
    logger.info("📝 Logging: Production mode" if DB_AVAILABLE else "Basic mode")
    logger.info("🔄 Starting polling...")
    logger.info("=" * 60)
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    run()
