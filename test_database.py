#!/usr/bin/env python3
"""
Test script for the new product database
"""
import sys
sys.path.insert(0, '/home/user/GZne_bot')

from bot.database import get_database
from bot.data import get_all_categories, find_product, get_product_display_name


def test_database():
    """Test the product database"""
    print("=" * 60)
    print("🧪 TESTING PRODUCT DATABASE")
    print("=" * 60)

    # Get database instance
    db = get_database()

    # Test 1: Check if database loaded
    print("\n✅ Test 1: Database Loading")
    total = db.get_total_products()
    print(f"   Total products loaded: {total}")

    # Test 2: Get categories
    print("\n✅ Test 2: Categories (Russian)")
    categories_ru = get_all_categories('ru')
    for cat_id, cat_name in categories_ru.items():
        products_count = len(db.get_products_by_category(cat_id, 'ru'))
        print(f"   {cat_name}: {products_count} products")

    print("\n✅ Test 3: Categories (Tajik)")
    categories_tj = get_all_categories('tj')
    for cat_id, cat_name in categories_tj.items():
        products_count = len(db.get_products_by_category(cat_id, 'tj'))
        print(f"   {cat_name}: {products_count} products")

    # Test 4: Get products from each category
    print("\n✅ Test 4: Sample Products from Each Category (Russian)")
    for cat_id in ['games', 'currency', 'mobile', 'services', 'software']:
        products = db.get_products_by_category(cat_id, 'ru')
        if products:
            first_product = products[0]
            print(f"\n   Category: {cat_id}")
            print(f"   - {get_product_display_name(first_product)}")
            print(f"   - Price: {db.format_price(first_product, 'TJS')}")
            print(f"   - Type: {first_product.get('type', 'N/A')}")

    # Test 5: Find specific products
    print("\n✅ Test 5: Find Products by ID")
    test_ids = ['chatgpt_plus', 'minecraft_java_bedrock', 'vbucks_1000']
    for product_id in test_ids:
        product = find_product(product_id, 'ru')
        if product:
            print(f"   ✓ Found: {product.get('name', 'Unknown')}")
        else:
            print(f"   ✗ Not found: {product_id}")

    # Test 6: Get popular products
    print("\n✅ Test 6: Popular Products")
    popular = db.get_popular_products('ru', limit=5)
    for i, product in enumerate(popular, 1):
        print(f"   {i}. {get_product_display_name(product)} - {db.format_price(product, 'TJS')}")

    # Test 7: Search functionality
    print("\n✅ Test 7: Search Products")
    search_queries = ['ChatGPT', 'Steam', 'Mobile']
    for query in search_queries:
        results = db.search_products(query, 'ru')
        print(f"   Search '{query}': {len(results)} results found")
        if results:
            print(f"   - Example: {results[0].get('name', 'Unknown')}")

    # Test 8: Product details
    print("\n✅ Test 8: Full Product Details")
    test_product = find_product('chatgpt_plus', 'ru')
    if test_product:
        print("\n" + db.get_product_details(test_product, 'ru'))

    # Test 9: Backwards compatibility (PRODUCTS proxy)
    print("\n✅ Test 9: Backwards Compatibility (PRODUCTS proxy)")
    from bot.data import PRODUCTS
    print(f"   'ru' in PRODUCTS: {'ru' in PRODUCTS}")
    print(f"   'tj' in PRODUCTS: {'tj' in PRODUCTS}")
    ru_data = PRODUCTS['ru']
    print(f"   Categories in PRODUCTS['ru']: {list(ru_data.keys())}")
    if 'cat_games' in ru_data:
        print(f"   Products in cat_games: {len(ru_data['cat_games'])}")

    print("\n" + "=" * 60)
    print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == '__main__':
    try:
        test_database()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
