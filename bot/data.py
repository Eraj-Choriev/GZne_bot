"""
Data utility functions - Clean and organized
Uses structured database from database.py
"""
import random
from typing import Dict, Any, List, Optional

# Import the new database
from .database import (
    get_database,
    get_categories,
    get_products_by_category,
    get_product_by_id,
    search_products,
    get_popular_products
)


def generate_order_id() -> str:
    """Generate a unique order ID"""
    return f"ORD-{random.randint(10000, 99999)}"


def generate_product_key() -> str:
    """Generate a fake product key for demonstration"""
    parts = []
    for _ in range(4):
        parts.append("".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=4)))
    return "-".join(parts)


# ============================================
# CATEGORY MANAGEMENT
# ============================================

CATEGORY_ICONS = {
    'games': '🎮',
    'currency': '💰',
    'mobile': '📱',
    'services': '⭐',
    'software': '💻',
}


def get_all_categories(lang: str = 'ru') -> Dict[str, str]:
    """
    Get all product categories with localized names

    Args:
        lang: Language code (ru or tj)

    Returns:
        Dict mapping category_id -> category_name
    """
    return get_categories(lang)


def get_category_name(category_id: str, lang: str = 'ru') -> str:
    """Get localized category name"""
    categories = get_categories(lang)
    return categories.get(category_id, category_id)


# ============================================
# PRODUCT ACCESS FUNCTIONS
# ============================================

def get_all_products_in_category(category_id: str, lang: str = 'ru') -> List[Dict[str, Any]]:
    """
    Get all products in a specific category

    Args:
        category_id: Category identifier (games, currency, mobile, services, software)
        lang: Language code (ru or tj)

    Returns:
        List of product dictionaries
    """
    return get_products_by_category(category_id, lang)


def find_product(product_id: str, lang: str = 'ru') -> Optional[Dict[str, Any]]:
    """
    Find a product by its ID

    Args:
        product_id: Unique product identifier
        lang: Language code (ru or tj)

    Returns:
        Product dictionary or None if not found
    """
    return get_product_by_id(product_id, lang)


# ============================================
# PRODUCT DISPLAY FUNCTIONS
# ============================================

def get_product_display_name(product: Dict[str, Any]) -> str:
    """
    Get beautifully formatted product name with icon and badges

    Args:
        product: Product dictionary

    Returns:
        Formatted string like "🎮 ChatGPT Plus 🔥"
    """
    db = get_database()
    return db.get_product_display_name(product)


def format_price(price: float, currency: str = 'TJS') -> str:
    """
    Format price with currency symbol

    Args:
        price: Price value
        currency: Currency code (TJS or USD)

    Returns:
        Formatted price string
    """
    if currency == 'USD':
        return f"💵 {price:.2f} USD"
    else:
        return f"💵 {price:.2f} TJS"


def get_product_price(product: Dict[str, Any], currency: str = 'TJS') -> str:
    """
    Get formatted product price

    Args:
        product: Product dictionary
        currency: Currency code (TJS or USD)

    Returns:
        Formatted price string
    """
    db = get_database()
    return db.format_price(product, currency)


def get_product_details(product: Dict[str, Any], lang: str = 'ru') -> str:
    """
    Get full formatted product details

    Args:
        product: Product dictionary
        lang: Language code

    Returns:
        Multi-line formatted product description
    """
    db = get_database()
    return db.get_product_details(product, lang)


# ============================================
# PRODUCT TYPE BADGES
# ============================================

TYPE_BADGES = {
    'Подписка': '🔄',
    'Обуна': '🔄',
    'Подарочная карта': '🎁',
    'Корти тӯҳфа': '🎁',
    'Валюта': '💵',
    'Асъор': '💵',
    'Лицензия': '🔑',
    'Иҷозатнома': '🔑',
    'Аренда': '⏰',
    'Иҷора': '⏰',
    'Аккаунт': '👤',
    'Ҳисоб': '👤',
}


def get_product_type_badge(product_type: str) -> str:
    """Get visual badge for product type"""
    return TYPE_BADGES.get(product_type, '📦')


# ============================================
# DELIVERY BADGES
# ============================================

DELIVERY_BADGE = '⚡'
INSTANT_DELIVERY = '🚀'


def get_delivery_badge(delivery_text: str) -> str:
    """Get appropriate delivery speed badge"""
    if not delivery_text:
        return DELIVERY_BADGE

    delivery_lower = delivery_text.lower()
    if any(word in delivery_lower for word in ['мгновенно', 'фавран', 'instant', '24/7', 'автоматически', 'худкор']):
        return INSTANT_DELIVERY
    return DELIVERY_BADGE


# ============================================
# BACKWARDS COMPATIBILITY
# ============================================

# For any code that still expects PRODUCTS dict
class ProductsProxy:
    """Proxy object that mimics the old PRODUCTS dict structure"""

    def __getitem__(self, lang: str) -> Dict[str, List[Dict[str, Any]]]:
        """Get products for a language, organized by category"""
        db = get_database()
        result = {}

        # Map old category keys to new ones
        category_mapping = {
            'cat_games': 'games',
            'cat_currency': 'currency',
            'cat_mobile': 'mobile',
            'cat_services': 'services',
            'cat_software': 'software',
        }

        for old_key, new_key in category_mapping.items():
            result[old_key] = db.get_products_by_category(new_key, lang)

        return result

    def get(self, lang: str, default=None) -> Dict[str, List[Dict[str, Any]]]:
        """Get products with default fallback"""
        try:
            return self[lang]
        except:
            return default or {}

    def __contains__(self, lang: str) -> bool:
        """Check if language is supported"""
        return lang in ['ru', 'tj']

    def keys(self):
        """Get supported languages"""
        return ['ru', 'tj']


# Create the proxy instance
PRODUCTS = ProductsProxy()


# ============================================
# ICON MAPPINGS (for backwards compatibility)
# ============================================

PRODUCT_ICONS = {
    'chatgpt': '🤖',
    'youtube1': '▶️',
    'spotify3': '🎵',
    'netflix1': '🎬',
    'steam50': '🎮',
    'xbox_pass': '🎯',
    'vbucks5000': '🔥',
    'robux4500': '🔷',
    'ml_diamonds': '💠',
    'pubg3000': '🎖️',
    'genshin6480': '⚡',
    'office365': '📊',
    'adobe_cc': '🎨',
}
