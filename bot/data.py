import random
from typing import Dict, Any


def generate_order_id() -> str:
    """Generate a unique order ID."""
    return f"ORD-{random.randint(10000, 99999)}"


def generate_product_key() -> str:
    """Generate a fake product key for demonstration."""
    parts = []
    for _ in range(4):
        parts.append("".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=4)))
    return "-".join(parts)


# ============================================
# PREMIUM 3D ICON SYSTEM (Jobs-Style Visual Excellence)
# ============================================
PRODUCT_ICONS = {
    # AI & Subscriptions
    'chatgpt': '🤖',
    'youtube1': '▶️',
    'spotify3': '🎵',
    'netflix1': '🎬',
    
    # Gaming Platforms
    'steam50': '🎮',
    'xbox_pass': '🎯',
    
    # Game Currencies
    'vbucks5000': '🔥',
    'robux4500': '🔷',
    'ml_diamonds': '💠',
    'pubg3000': '🎖️',
    'genshin6480': '⚡',
    
    # Professional Software
    'office365': '📊',
    'adobe_cc': '🎨',
}

CATEGORY_ICONS = {
    'cat_games': '🎮',
    'cat_currency': '💰',
    'cat_mobile': '📱',
    'cat_services': '⭐',
    'cat_software': '💻',
}

# Product type badges for enhanced visual hierarchy
TYPE_BADGES = {
    'Подписка': '🔄',
    'Обуна': '🔄',
    'Подарочная карта': '🎁',
    'Корти тӯҳфа': '🎁',
    'Валюта': '💵',
    'Асъор': '💵',
    'Лицензия': '🔑',
    'Иҷозатнома': '🔑',
}

# Delivery speed indicators
DELIVERY_BADGE = '⚡'
INSTANT_DELIVERY = '🚀'


# ============================================
# ENHANCED PRODUCT DATABASE
# ============================================
PRODUCTS = {
    'ru': {
        'cat_games': [
            {
                'id': 'chatgpt',
                'name': 'ChatGPT Plus',
                'price': 20,
                'type': 'Подписка',
                'validity': '1 месяц',
                'delivery': '20-30 минут после подтверждения оплаты',
                'icon': '🤖',
                'description': 'Полный доступ к ChatGPT-4, быстрые ответы, приоритетная поддержка',
                'popular': True,
                'discount': None
            },
            {
                'id': 'steam50',
                'name': 'Steam Gift Card $50',
                'price': 52,
                'type': 'Подарочная карта',
                'validity': 'Бессрочно',
                'delivery': '20-30 минут после подтверждения оплаты',
                'icon': '🎮',
                'description': 'Пополните Steam кошелек на $50 и купите любые игры',
                'popular': True,
                'discount': None
            },
            {
                'id': 'xbox_pass',
                'name': 'Xbox Game Pass',
                'price': 35,
                'type': 'Подписка',
                'validity': '3 месяца',
                'delivery': '20-30 минут после подтверждения оплаты',
                'icon': '🎯',
                'description': 'Доступ к 100+ играм на Xbox и ПК',
                'popular': False,
                'discount': 15
            },
        ],
        'cat_currency': [
            {
                'id': 'vbucks5000',
                'name': 'Fortnite V-Bucks 5000',
                'price': 40,
                'type': 'Валюта',
                'validity': 'N/A',
                'delivery': '20-30 минут после подтверждения оплаты',
                'icon': '🔥',
                'description': '5000 V-Bucks для покупки скинов и Battle Pass',
                'popular': True,
                'discount': None
            },
            {
                'id': 'robux4500',
                'name': 'Roblox 4500 Robux',
                'price': 50,
                'type': 'Валюта',
                'validity': 'N/A',
                'delivery': '20-30 минут после подтверждения оплаты',
                'icon': '🔷',
                'description': '4500 Robux для кастомизации аватара и покупок',
                'popular': True,
                'discount': None
            },
            {
                'id': 'ml_diamonds',
                'name': 'Mobile Legends 2000 Diamonds',
                'price': 25,
                'type': 'Валюта',
                'validity': 'N/A',
                'delivery': '20-30 минут после подтверждения оплаты',
                'icon': '💠',
                'description': '2000 алмазов для героев и скинов',
                'popular': False,
                'discount': None
            },
        ],
        'cat_mobile': [
            {
                'id': 'pubg3000',
                'name': 'PUBG Mobile UC 3000',
                'price': 30,
                'type': 'Валюта',
                'validity': 'N/A',
                'delivery': '10 минут после подтверждения оплаты',
                'icon': '🎖️',
                'description': '3000 UC для Royal Pass и эксклюзивных предметов',
                'popular': False,
                'discount': None
            },
            {
                'id': 'genshin6480',
                'name': 'Genshin Impact Crystal 6480',
                'price': 100,
                'type': 'Валюта',
                'validity': 'N/A',
                'delivery': '20-3 минут после подтверждения оплаты',
                'icon': '⚡',
                'description': '6480 кристаллов Genesis для желаний и персонажей',
                'popular': True,
                'discount': 10
            },
        ],
        'cat_services': [
            {
                'id': 'vip_sub_1',
                'name': 'Подписка на 1 месяц',
                'price': 900,
                'old_price': 1800,
                'type': 'Подписка',
                'validity': '1 месяц',
                'delivery': 'Мгновенно',
                'icon': '🔥',
                'description': 'Горячий ВИП Sasha Beart (канал)\n\nЗдесь около 80% всех моих видео, поэтому, если ты не голодный извращенец, которому нужно всё и сразу и много, то для знакомства с моим творчеством тебе этого вполне хватит. А уже дальше решишь, стоит ли со мной оставаться ещё или нет😍 Я раскрою секрет - 90% подписавшихся на 1 мес потом оформляют годовую подписку!',
                'popular': True,
                'discount': 50
            },
            {
                'id': 'youtube1',
                'name': 'YouTube Premium',
                'price': 12,
                'type': 'Подписка',
                'validity': '1 месяц',
                'delivery': '20-30 минут после подтверждения оплаты',
                'icon': '▶️',
                'description': 'Без рекламы, фоновое воспроизведение, YouTube Music',
                'popular': True,
                'discount': None
            },
            {
                'id': 'spotify3',
                'name': 'Spotify Premium',
                'price': 30,
                'type': 'Подписка',
                'validity': '3 месяца',
                'delivery': '20-30 минут после подтверждения оплаты',
                'icon': '🎵',
                'description': 'Музыка без рекламы, офлайн-режим, высокое качество',
                'popular': True,
                'discount': None
            },
            {
                'id': 'netflix1',
                'name': 'Netflix Premium',
                'price': 15,
                'type': 'Подписка',
                'validity': '1 месяц',
                'delivery': '20-30 минут после подтверждения оплаты',
                'icon': '🎬',
                'description': '4K качество, 4 экрана одновременно',
                'popular': False,
                'discount': None
            },
        ],
        'cat_software': [
            {
                'id': 'office365',
                'name': 'Microsoft Office 365',
                'price': 80,
                'type': 'Лицензия',
                'validity': '1 год',
                'delivery': '20-30 минут после подтверждения оплаты',
                'icon': '📊',
                'description': 'Word, Excel, PowerPoint, 1TB OneDrive',
                'popular': True,
                'discount': None
            },
            {
                'id': 'adobe_cc',
                'name': 'Adobe Creative Cloud',
                'price': 55,
                'type': 'Подписка',
                'validity': '1 месяц',
                'delivery': '20-30 минут после подтверждения оплаты',
                'icon': '🎨',
                'description': 'Photoshop, Illustrator, Premiere Pro и все приложения',
                'popular': True,
                'discount': None
            },
        ]
    },
    'tj': {
        'cat_games': [
            {
                'id': 'chatgpt',
                'name': 'ChatGPT Plus',
                'price': 20,
                'type': 'Обуна',
                'validity': '1 моҳ',
                'delivery': '20-30 дақиқа баъд аз тасдиқи пардохт',
                'icon': '🤖',
                'description': 'Дастрасии пурра ба ChatGPT-4, ҷавобҳои тез, дастгирии афзалиятнок',
                'popular': True,
                'discount': None
            },
            {
                'id': 'steam50',
                'name': 'Steam Gift Card $50',
                'price': 52,
                'type': 'Корти тӯҳфа',
                'validity': 'Бемаҳдуд',
                'delivery': '20-30 дақиқа баъд аз тасдиқи пардохт',
                'icon': '🎮',
                'description': 'Ҳамёни Steam-ро ба $50 пур кунед ва бозиҳои дилхоҳро харед',
                'popular': True,
                'discount': None
            },
            {
                'id': 'xbox_pass',
                'name': 'Xbox Game Pass',
                'price': 35,
                'type': 'Обуна',
                'validity': '3 моҳ',
                'delivery': '20-30 дақиқа баъд аз тасдиқи пардохт',
                'icon': '🎯',
                'description': 'Дастрасӣ ба 100+ бозиҳо дар Xbox ва PC',
                'popular': False,
                'discount': 15
            },
        ],
        'cat_currency': [
            {
                'id': 'vbucks5000',
                'name': 'Fortnite V-Bucks 5000',
                'price': 40,
                'type': 'Асъор',
                'validity': 'N/A',
                'delivery': '20-30 дақиқа баъд аз тасдиқи пардохт',
                'icon': '🔥',
                'description': '5000 V-Bucks барои харидани скинҳо ва Battle Pass',
                'popular': True,
                'discount': None
            },
            {
                'id': 'robux4500',
                'name': 'Roblox 4500 Robux',
                'price': 50,
                'type': 'Асъор',
                'validity': 'N/A',
                'delivery': '20-30 дақиқа баъд аз тасдиқи пардохт',
                'icon': '🔷',
                'description': '4500 Robux барои фармоишдиҳии аватар ва хариднокӣ',
                'popular': True,
                'discount': None
            },
            {
                'id': 'ml_diamonds',
                'name': 'Mobile Legends 2000 Diamonds',
                'price': 25,
                'type': 'Асъор',
                'validity': 'N/A',
                'delivery': '20-30 дақиқа баъд аз тасдиқи пардохт',
                'icon': '💠',
                'description': '2000 олмос барои қаҳрамонҳо ва скинҳо',
                'popular': False,
                'discount': None
            },
        ],
        'cat_mobile': [
            {
                'id': 'pubg3000',
                'name': 'PUBG Mobile UC 3000',
                'price': 30,
                'type': 'Асъор',
                'validity': 'N/A',
                'delivery': '20-30 дақиқа баъд аз тасдиқи пардохт',
                'icon': '🎖️',
                'description': '3000 UC барои Royal Pass ва ашёҳои махсус',
                'popular': False,
                'discount': None
            },
            {
                'id': 'genshin6480',
                'name': 'Genshin Impact Crystal 6480',
                'price': 100,
                'type': 'Асъор',
                'validity': 'N/A',
                'delivery': '20-30 дақиқа баъд аз тасдиқи пардохт',
                'icon': '⚡',
                'description': '6480 кристалли Genesis барои хоҳишҳо ва персонажҳо',
                'popular': True,
                'discount': 10
            },
        ],
        'cat_services': [
            {
                'id': 'youtube1',
                'name': 'YouTube Premium',
                'price': 12,
                'type': 'Обуна',
                'validity': '1 моҳ',
                'delivery': '20-30 дақиқа баъд аз тасдиқи пардохт',
                'icon': '▶️',
                'description': 'Бе реклама, пахши замина, YouTube Music',
                'popular': True,
                'discount': None
            },
            {
                'id': 'spotify3',
                'name': 'Spotify Premium',
                'price': 30,
                'type': 'Обуна',
                'validity': '3 моҳ',
                'delivery': '20-30 дақиқа баъд аз тасдиқи пардохт',
                'icon': '🎵',
                'description': 'Мусиқӣ бе реклама, реҷаи офлайн, сифати баланд',
                'popular': True,
                'discount': None
            },
            {
                'id': 'netflix1',
                'name': 'Netflix Premium',
                'price': 15,
                'type': 'Обуна',
                'validity': '1 моҳ',
                'delivery': '20-30 дақиқа баъд аз тасдиқи пардохт',
                'icon': '🎬',
                'description': 'Сифати 4K, 4 экран якбора',
                'popular': False,
                'discount': None
            },
        ],
        'cat_software': [
            {
                'id': 'office365',
                'name': 'Microsoft Office 365',
                'price': 80,
                'type': 'Иҷозатнома',
                'validity': '1 сол',
                'delivery': '20-30 дақиқа баъд аз тасдиқи пардохт',
                'icon': '📊',
                'description': 'Word, Excel, PowerPoint, 1TB OneDrive',
                'popular': True,
                'discount': None
            },
            {
                'id': 'adobe_cc',
                'name': 'Adobe Creative Cloud',
                'price': 55,
                'type': 'Обуна',
                'validity': '1 моҳ',
                'delivery': '20-30 дақиқа баъд аз тасдиқи пардохт',
                'icon': '🎨',
                'description': 'Photoshop, Illustrator, Premiere Pro ва ҳамаи барномаҳо',
                'popular': True,
                'discount': None
            },
        ]
    }
}


def find_product(lang: str, product_id: str) -> Dict[str, Any] | None:
    """Find a product by its ID for a given language."""
    for category_list in PRODUCTS[lang].values():
        for product in category_list:
            if product['id'] == product_id:
                return product
    return None


def get_product_display_name(product: Dict[str, Any]) -> str:
    """
    Get beautifully formatted product name with icon and badges.
    Ogilvy principle: Make every word count.
    """
    icon = product.get('icon', '📦')
    name = product['name']
    
    badges = []
    
    # Add popular badge
    if product.get('popular'):
        badges.append('🔥')
    
    # Add discount badge
    if product.get('discount'):
        badges.append(f'🏷️-{product["discount"]}%')
    
    badge_str = ' '.join(badges)
    
    if badge_str:
        return f"{icon} {name} {badge_str}"
    return f"{icon} {name}"


def get_product_type_badge(product_type: str) -> str:
    """Get visual badge for product type."""
    return TYPE_BADGES.get(product_type, '📦')


def format_price(price: float, lang: str = 'ru') -> str:
    """
    Format price with proper currency symbol and styling.
    Jobs principle: Sweat the details.
    """
    if lang == 'ru':
        return f"💵 {price} USD"
    else:  # tj
        return f"💵 {price} USD"


def get_delivery_badge(delivery_text: str) -> str:
    """Get appropriate delivery speed badge."""
    if '20-30' in delivery_text or 'instant' in delivery_text.lower():
        return INSTANT_DELIVERY
    return DELIVERY_BADGE