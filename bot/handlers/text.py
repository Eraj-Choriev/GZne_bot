from telegram import Update
from telegram.ext import ContextTypes

from ..state import USER_DATA, get_user_lang
from ..localization import get_locale
from .receipt import invalid_receipt_handler
from .navigation import handle_category, handle_info
from .support import cmd_support
from .language import cmd_language


async def main_text_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Main router for text messages based on user state."""
    user_id = update.effective_user.id
    state = USER_DATA.get(user_id, {}).get('state')
    
    if state == 'awaiting_receipt':
        await invalid_receipt_handler(update, context)
        return
    
    # If not in a specific state, treat text as a menu command
    await menu_text_handler(update, context)


async def menu_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle taps on the persistent reply keyboard by matching localized labels."""
    user_id = update.effective_user.id
    lang = get_user_lang(user_id)
    L = get_locale(lang)
    
    text = (update.message.text or '').strip()
    
    # Map localized button text to actions
    mapping = {
        L['cat_info_btn']: 'cat_info',
        L['cat_games_btn']: 'cat_games',
        L['cat_currency_btn']: 'cat_currency',
        L['cat_mobile_btn']: 'cat_mobile',
        L['cat_services_btn']: 'cat_services',
        L['cat_software_btn']: 'cat_software',
        L['change_lang_btn']: 'change_lang',
        L['support_btn']: 'cat_support',
    }
    
    action = mapping.get(text)
    
    if not action:
        await update.message.reply_text(L['unknown_command'])
        return
    
    # To avoid circular imports and complex logic, we create a fake query object
    # and call the appropriate handler. A more robust solution might use a
    # state machine or a more advanced router.
    class FakeQuery:
        def __init__(self):
            self.data = action
            self.message = update.message
            self.from_user = update.effective_user
        
        async def answer(self, *args, **kwargs):
            pass
    
    # Create a fake update object with the fake query
    fake_update = type('FakeUpdate', (), {'callback_query': FakeQuery()})()
    
    # Route to appropriate handler based on action
    if action == 'cat_info':
        await handle_info(fake_update, context)
    elif action.startswith('cat_') and action != 'cat_support':
        await handle_category(fake_update, context)
    elif action == 'change_lang':
        await cmd_language(update, context)
    elif action == 'cat_support':
        await cmd_support(update, context)