#!/usr/bin/env python3
"""
Тестовый скрипт для проверки подключения базы данных
"""
import sys
sys.path.insert(0, '/home/user/GZne_bot')

from bot.models import (
    init_db,
    create_user,
    create_order,
    update_order_status,
    get_user_orders,
    track_event,
    get_session
)


def test_database():
    """Тест базы данных"""
    print("=" * 60)
    print("🧪 ТЕСТИРОВАНИЕ БАЗЫ ДАННЫХ")
    print("=" * 60)

    # Тест 1: Инициализация БД
    print("\n✅ Тест 1: Инициализация базы данных")
    try:
        engine = init_db()
        print(f"   ✓ База данных инициализирована: data/bot.db")
        print(f"   ✓ Engine: {engine}")
    except Exception as e:
        print(f"   ✗ Ошибка: {e}")
        return False

    # Тест 2: Создание пользователя
    print("\n✅ Тест 2: Создание пользователя")
    try:
        user = create_user(
            telegram_id=123456789,
            username="test_user",
            first_name="Test",
            last_name="User",
            language="ru"
        )
        print(f"   ✓ Пользователь создан: {user}")
        print(f"   - Telegram ID: {user.telegram_id}")
        print(f"   - Username: {user.username}")
        print(f"   - Язык: {user.language}")
    except Exception as e:
        print(f"   ✗ Ошибка: {e}")
        return False

    # Тест 3: Создание заказа
    print("\n✅ Тест 3: Создание заказа")
    try:
        order = create_order(
            telegram_id=123456789,
            order_id="ORD-TEST-12345",
            product_id="chatgpt_plus",
            product_name="ChatGPT Plus",
            product_category="services",
            price_tjs=288.00,
            price_usd=27.17
        )
        print(f"   ✓ Заказ создан: {order}")
        print(f"   - Order ID: {order.order_id}")
        print(f"   - Продукт: {order.product_name}")
        print(f"   - Цена TJS: {order.price_tjs}")
        print(f"   - Статус: {order.status}")
    except Exception as e:
        print(f"   ✗ Ошибка: {e}")
        return False

    # Тест 4: Обновление статуса заказа
    print("\n✅ Тест 4: Обновление статуса заказа")
    try:
        result = update_order_status("ORD-TEST-12345", "confirmed", "Payment received")
        print(f"   ✓ Статус обновлен: {result}")
    except Exception as e:
        print(f"   ✗ Ошибка: {e}")
        return False

    # Тест 5: Получение заказов пользователя
    print("\n✅ Тест 5: Получение заказов пользователя")
    try:
        orders = get_user_orders(123456789)
        print(f"   ✓ Найдено заказов: {len(orders)}")
        for order in orders:
            print(f"   - {order.order_id}: {order.product_name} ({order.status})")
    except Exception as e:
        print(f"   ✗ Ошибка: {e}")
        return False

    # Тест 6: Трекинг событий
    print("\n✅ Тест 6: Трекинг событий аналитики")
    try:
        track_event(123456789, "test_event", "Test data")
        track_event(123456789, "purchase_initiated", "Product: ChatGPT Plus")
        print(f"   ✓ События сохранены")
    except Exception as e:
        print(f"   ✗ Ошибка: {e}")
        return False

    # Тест 7: Проверка таблиц
    print("\n✅ Тест 7: Проверка структуры таблиц")
    try:
        session = get_session()
        from bot.models import User, Order, Analytics

        user_count = session.query(User).count()
        order_count = session.query(Order).count()
        analytics_count = session.query(Analytics).count()

        print(f"   ✓ Таблица Users: {user_count} записей")
        print(f"   ✓ Таблица Orders: {order_count} записей")
        print(f"   ✓ Таблица Analytics: {analytics_count} записей")

        session.close()
    except Exception as e:
        print(f"   ✗ Ошибка: {e}")
        return False

    print("\n" + "=" * 60)
    print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    print("=" * 60)
    print("\n📊 Статистика:")
    print(f"   - Пользователей: {user_count}")
    print(f"   - Заказов: {order_count}")
    print(f"   - События аналитики: {analytics_count}")
    print(f"\n📁 Файл БД: data/bot.db")

    return True


if __name__ == '__main__':
    try:
        success = test_database()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
