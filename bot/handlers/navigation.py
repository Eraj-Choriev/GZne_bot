from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from ..state import USER_DATA, get_user_lang
from ..localization import get_locale
from ..keyboards import get_back_button
from ..data import PRODUCTS, find_product
from .start import send_main_menu


async def handle_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    L = get_locale(lang)
    keyboard = [[get_back_button(lang, 'main')]]
    await query.message.edit_text(
        f"**{L['info_title']}**\n\n{L['info_text']}",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN,
    )


async def handle_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_lang(user_id)
    L = get_locale(lang)
    category_key = query.data
    USER_DATA[user_id]['current_category'] = category_key
    products = PRODUCTS[lang].get(category_key, [])
    keyboard = []
    for product in products:
        keyboard.append([InlineKeyboardButton(product['name'], callback_data=f"prod_{product['id']}")])
    keyboard.append([get_back_button(lang, 'main')])
    await query.message.edit_text(
        L['select_product'],
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def handle_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_lang(user_id)
    L = get_locale(lang)
    product_id = query.data.split('_', 1)[1]
    USER_DATA[user_id]['current_product'] = product_id
    product = find_product(lang, product_id)
    if not product:
        raise ValueError(f"Product not found: {product_id}")
    # Calculate old price (fake discount logic for demo)
    price = product['price']
    old_price = product.get('old_price', price * 2)
    currency = "USD" # Using USD as default currency

    text = L['product_page_template'].format(
        name=product['name'],
        price=f"{price:.2f}",
        old_price=f"{old_price:.2f}",
        currency=currency,
        validity=product['validity'],
        description=product['description']
    )
    keyboard = [
        [InlineKeyboardButton(L['buy_btn'], callback_data=f"buy_{product_id}")],
        [get_back_button(lang, 'category')],
    ]
    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)


async def back_to_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    category_key = USER_DATA[user_id].get('current_category')
    if not category_key:
        await send_main_menu(query.message, context, get_user_lang(user_id))
        return

    # To avoid circular imports, we can't directly call the handler.
    # Instead, we can re-create a fake update and pass it to the handler.
    # A better solution would be a more robust routing system.
    class FakeQuery:
        data = category_key
        message = query.message
        from_user = query.from_user
        async def answer(self):
            pass
    await handle_category(type('U', (), {'callback_query': FakeQuery()})(), context)


async def back_to_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    product_id = USER_DATA[user_id].get('current_product')
    if not product_id:
        await send_main_menu(query.message, context, get_user_lang(user_id))
        return

    class FakeQuery:
        data = f"prod_{product_id}"
        message = query.message
        from_user = query.from_user
        async def answer(self):
            pass
    await handle_product(type('U', (), {'callback_query': FakeQuery()})(), context)