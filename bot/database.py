"""
Product Database Module - Clean and structured product management
Loads products from JSON file and provides easy access functions
"""
import json
import os
from typing import Dict, List, Optional, Any
from pathlib import Path


class ProductDatabase:
    """Structured product database with multi-language support"""

    def __init__(self):
        self._data: Dict = {}
        self._loaded = False

    def load(self) -> None:
        """Load products from JSON file"""
        if self._loaded:
            return

        json_path = Path(__file__).parent.parent / 'locales' / 'products.json'

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                self._data = json.load(f)
            self._loaded = True
            print(f"✅ Products database loaded: {self.get_total_products()} products")
        except FileNotFoundError:
            print(f"❌ Error: products.json not found at {json_path}")
            self._data = {"categories": {}, "products": {}}
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing products.json: {e}")
            self._data = {"categories": {}, "products": {}}

    def get_categories(self, lang: str = 'ru') -> Dict[str, str]:
        """
        Get all categories with their names in specified language

        Returns:
            Dict with category_id -> category_name mapping
        """
        if not self._loaded:
            self.load()

        categories = {}
        for cat_id, cat_data in self._data.get('categories', {}).items():
            categories[cat_id] = cat_data.get(lang, cat_data.get('ru', cat_id))
        return categories

    def get_category_icon(self, category_id: str) -> str:
        """Get icon for a category"""
        if not self._loaded:
            self.load()

        cat_data = self._data.get('categories', {}).get(category_id, {})
        return cat_data.get('icon', '📦')

    def get_products_by_category(self, category_id: str, lang: str = 'ru') -> List[Dict[str, Any]]:
        """
        Get all products in a specific category

        Args:
            category_id: Category identifier (games, currency, mobile, services, software)
            lang: Language code (ru or tj)

        Returns:
            List of product dictionaries with localized fields
        """
        if not self._loaded:
            self.load()

        products = self._data.get('products', {}).get(category_id, [])
        return [self._localize_product(p, lang) for p in products]

    def get_product_by_id(self, product_id: str, lang: str = 'ru') -> Optional[Dict[str, Any]]:
        """
        Find a product by its ID across all categories

        Args:
            product_id: Unique product identifier
            lang: Language code (ru or tj)

        Returns:
            Localized product dictionary or None if not found
        """
        if not self._loaded:
            self.load()

        for category_products in self._data.get('products', {}).values():
            for product in category_products:
                if product.get('id') == product_id:
                    return self._localize_product(product, lang)
        return None

    def search_products(self, query: str, lang: str = 'ru') -> List[Dict[str, Any]]:
        """
        Search products by name or description

        Args:
            query: Search query string
            lang: Language code (ru or tj)

        Returns:
            List of matching products
        """
        if not self._loaded:
            self.load()

        query_lower = query.lower()
        results = []

        for category_products in self._data.get('products', {}).values():
            for product in category_products:
                product_name = product.get('name', {}).get(lang, '').lower()
                product_desc = product.get('description', {}).get(lang, '').lower()

                if query_lower in product_name or query_lower in product_desc:
                    results.append(self._localize_product(product, lang))

        return results

    def get_popular_products(self, lang: str = 'ru', limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get popular products across all categories

        Args:
            lang: Language code (ru or tj)
            limit: Maximum number of products to return

        Returns:
            List of popular products
        """
        if not self._loaded:
            self.load()

        popular = []
        for category_products in self._data.get('products', {}).values():
            for product in category_products:
                if product.get('popular', False):
                    popular.append(self._localize_product(product, lang))

        return popular[:limit]

    def get_total_products(self) -> int:
        """Get total number of products in database"""
        if not self._loaded:
            self.load()

        total = 0
        for category_products in self._data.get('products', {}).values():
            total += len(category_products)
        return total

    def _localize_product(self, product: Dict[str, Any], lang: str) -> Dict[str, Any]:
        """
        Convert product to use simple string fields instead of nested lang objects

        Args:
            product: Product dictionary with nested language objects
            lang: Target language code

        Returns:
            Flattened product dictionary with localized strings
        """
        localized = product.copy()

        # Localize fields that have language variants
        for field in ['name', 'type', 'delivery', 'description', 'validity']:
            if field in product and isinstance(product[field], dict):
                localized[field] = product[field].get(lang, product[field].get('ru', ''))

        return localized

    def get_product_display_name(self, product: Dict[str, Any]) -> str:
        """
        Get formatted product name with icon and badges

        Args:
            product: Product dictionary

        Returns:
            Formatted string like "🎮 ChatGPT Plus 🔥"
        """
        icon = product.get('icon', '📦')
        name = product.get('name', 'Unknown Product')

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

    def format_price(self, product: Dict[str, Any], currency: str = 'TJS') -> str:
        """
        Format product price with currency symbol

        Args:
            product: Product dictionary
            currency: Currency code (TJS or USD)

        Returns:
            Formatted price string like "💵 323.90 TJS"
        """
        if currency == 'USD':
            price = product.get('price_usd', 0)
            return f"💵 {price:.2f} USD"
        else:
            price = product.get('price_tjs', 0)
            return f"💵 {price:.2f} TJS"

    def get_product_details(self, product: Dict[str, Any], lang: str = 'ru') -> str:
        """
        Get formatted product details for display

        Args:
            product: Product dictionary
            lang: Language code

        Returns:
            Formatted multi-line product description
        """
        lines = [
            self.get_product_display_name(product),
            "",
            f"📝 {product.get('description', 'Нет описания')}",
            "",
            f"💰 Цена: {self.format_price(product, 'TJS')} ({self.format_price(product, 'USD')})",
            f"📦 Тип: {product.get('type', 'N/A')}",
            f"🎮 Платформа: {product.get('platform', 'N/A')}",
            f"⚡ Доставка: {product.get('delivery', 'N/A')}",
            f"⏰ Срок действия: {product.get('validity', 'N/A')}",
        ]

        return "\n".join(lines)


# Global database instance
_db = ProductDatabase()


def get_database() -> ProductDatabase:
    """Get the global product database instance"""
    if not _db._loaded:
        _db.load()
    return _db


# Convenience functions for backward compatibility
def get_categories(lang: str = 'ru') -> Dict[str, str]:
    """Get all product categories"""
    return get_database().get_categories(lang)


def get_products_by_category(category_id: str, lang: str = 'ru') -> List[Dict[str, Any]]:
    """Get products in a category"""
    return get_database().get_products_by_category(category_id, lang)


def get_product_by_id(product_id: str, lang: str = 'ru') -> Optional[Dict[str, Any]]:
    """Find product by ID"""
    return get_database().get_product_by_id(product_id, lang)


def search_products(query: str, lang: str = 'ru') -> List[Dict[str, Any]]:
    """Search products"""
    return get_database().search_products(query, lang)


def get_popular_products(lang: str = 'ru', limit: int = 10) -> List[Dict[str, Any]]:
    """Get popular products"""
    return get_database().get_popular_products(lang, limit)
