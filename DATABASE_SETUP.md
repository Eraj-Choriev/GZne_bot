# 📊 Пошаговая инструкция: Подключение базы данных к боту

Эта инструкция покажет вам, как подключить и использовать базу данных SQLite в вашем Telegram боте.

---

## 🎯 Что дает база данных?

✅ **Сохранение заказов** - все заказы пользователей в БД
✅ **Профили пользователей** - информация о каждом пользователе
✅ **Аналитика** - отслеживание действий пользователей
✅ **История покупок** - просмотр всех заказов пользователя
✅ **Статистика** - количество заказов, популярные товары

---

## 📋 Шаг 1: Установка зависимостей

### На вашем Mac:

```bash
cd /Users/eraj2/Desktop/new_version/GZne_bot

# Установите зависимости
pip install sqlalchemy alembic

# Или установите все из requirements.txt
pip install -r requirements.txt
```

### Проверка установки:

```bash
python -c "import sqlalchemy; print(sqlalchemy.__version__)"
```

Должно вывести версию SQLAlchemy (например: `2.0.25`)

---

## 📊 Шаг 2: Тестирование подключения БД

Запустите тестовый скрипт:

```bash
cd /Users/eraj2/Desktop/new_version/GZne_bot
python test_db_connection.py
```

### Ожидаемый результат:

```
============================================================
🧪 ТЕСТИРОВАНИЕ БАЗЫ ДАННЫХ
============================================================

✅ Тест 1: Инициализация базы данных
   ✓ База данных инициализирована: data/bot.db
   ✓ Engine: Engine(sqlite:///data/bot.db)

✅ Тест 2: Создание пользователя
   ✓ Пользователь создан: <User(telegram_id=123456789, username=test_user)>
   - Telegram ID: 123456789
   - Username: test_user
   - Язык: ru

✅ Тест 3: Создание заказа
   ✓ Заказ создан: <Order(order_id=ORD-TEST-12345, status=pending)>
   - Order ID: ORD-TEST-12345
   - Продукт: ChatGPT Plus
   - Цена TJS: 288.0
   - Статус: pending

✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!
============================================================
```

Если вы видите это - **база данных работает!** ✅

---

## 🚀 Шаг 3: Запуск бота с базой данных

### Запустите бота:

```bash
cd /Users/eraj2/Desktop/new_version/GZne_bot
python run.py
```

### Вы должны увидеть:

```
============================================================
🚀 GZne Bot started successfully!
============================================================
📊 Database: Enabled ✅
📝 Logging: Production mode
🔄 Starting polling...
============================================================
✅ Production logging initialized
✅ Database initialized successfully
✅ Locales loaded
✅ Config loaded for admin: gzone_admin_ctrl
```

**Если видите "Database: Enabled ✅" - всё работает!** 🎉

---

## 📁 Шаг 4: Проверка файлов базы данных

После запуска бота должны появиться новые директории и файлы:

```bash
# Проверьте структуру
ls -la data/
ls -la logs/

# Должны увидеть:
# data/bot.db          <- База данных SQLite
# logs/bot.log         <- Общие логи
# logs/errors.log      <- Логи ошибок
```

### Просмотр содержимого БД:

```bash
# Установите sqlite3 (если нет)
brew install sqlite3  # для Mac

# Откройте БД
sqlite3 data/bot.db

# SQL команды для просмотра:
.tables                    # Список таблиц
SELECT * FROM users;       # Все пользователи
SELECT * FROM orders;      # Все заказы
SELECT * FROM analytics;   # Аналитика
.quit                      # Выход
```

---

## 🧪 Шаг 5: Тестирование с реальным пользователем

### 1. Запустите бота:
```bash
python run.py
```

### 2. Откройте Telegram и найдите вашего бота

### 3. Выполните действия:
1. Отправьте `/start`
2. Выберите категорию товаров
3. Выберите товар
4. Нажмите "Купить"
5. Выберите способ оплаты

### 4. Проверьте БД:

```bash
# Откройте БД
sqlite3 data/bot.db

# Проверьте пользователей
SELECT * FROM users;

# Проверьте заказы
SELECT order_id, product_name, status, price_tjs FROM orders;

# Проверьте аналитику
SELECT event_type, COUNT(*) as count FROM analytics GROUP BY event_type;

.quit
```

Вы должны увидеть:
- Вашего пользователя в таблице `users`
- Созданный заказ в таблице `orders`
- События в таблице `analytics`

---

## 📊 Шаг 6: Что сохраняется в БД?

### Таблица `users`:
```
id | telegram_id | username | first_name | language | created_at | last_active
```

### Таблица `orders`:
```
id | order_id | product_id | product_name | price_tjs | status | created_at
```

### Таблица `analytics`:
```
id | user_telegram_id | event_type | event_data | created_at
```

---

## 🔍 Шаг 7: Просмотр логов

### Общие логи:
```bash
tail -f logs/bot.log
```

Вы увидите:
```
2024-12-06 18:00:00 - bot.handlers.purchase - INFO - ✅ Order ORD-12345 saved to database for user 123456789
2024-12-06 18:00:05 - bot.models - INFO - ✅ User 123456789 created
```

### Логи ошибок:
```bash
tail -f logs/errors.log
```

---

## 💡 Шаг 8: Использование БД в своем коде

### Пример 1: Получить заказы пользователя

```python
from bot.models import get_user_orders

# В вашем handler
user_id = update.effective_user.id
orders = get_user_orders(user_id, limit=10)

for order in orders:
    print(f"Заказ {order.order_id}: {order.product_name} - {order.status}")
```

### Пример 2: Создать новый заказ

```python
from bot.models import create_order

order = create_order(
    telegram_id=user_id,
    order_id="ORD-12345",
    product_id="chatgpt_plus",
    product_name="ChatGPT Plus",
    product_category="services",
    price_tjs=288.00,
    price_usd=27.17
)
```

### Пример 3: Обновить статус заказа

```python
from bot.models import update_order_status

# После подтверждения оплаты
update_order_status("ORD-12345", "confirmed", "Payment received")

# После выполнения заказа
update_order_status("ORD-12345", "completed", "Product delivered")
```

### Пример 4: Отследить событие

```python
from bot.models import track_event

# Отследить действие пользователя
track_event(user_id, "product_viewed", "Product: ChatGPT Plus")
track_event(user_id, "purchase_initiated", "Order: ORD-12345")
```

---

## 📈 Шаг 9: Просмотр статистики

### Python скрипт для статистики:

```python
#!/usr/bin/env python3
from bot.models import get_session, User, Order, Analytics

session = get_session()

# Общая статистика
total_users = session.query(User).count()
total_orders = session.query(Order).count()
pending_orders = session.query(Order).filter_by(status='pending').count()
completed_orders = session.query(Order).filter_by(status='completed').count()

print(f"👥 Пользователей: {total_users}")
print(f"📦 Заказов: {total_orders}")
print(f"⏳ В ожидании: {pending_orders}")
print(f"✅ Выполнено: {completed_orders}")

session.close()
```

Сохраните как `stats.py` и запустите:
```bash
python stats.py
```

---

## 🔧 Troubleshooting (Решение проблем)

### Проблема 1: "ModuleNotFoundError: No module named 'sqlalchemy'"

**Решение:**
```bash
pip install sqlalchemy
```

### Проблема 2: База данных не создается

**Решение:**
```bash
# Создайте директорию вручную
mkdir -p data

# Проверьте права
chmod 755 data

# Запустите тест
python test_db_connection.py
```

### Проблема 3: "Database: Disabled ⚠️" при запуске

**Решение:**
```bash
# Проверьте что файлы существуют
ls bot/models.py
ls bot/logger.py

# Если нет - скачайте их из репозитория
git pull
```

### Проблема 4: Ошибки при сохранении заказа

**Решение:**
```bash
# Проверьте логи
tail -20 logs/errors.log

# Пересоздайте БД
rm data/bot.db
python test_db_connection.py
```

---

## ✅ Checklist (Проверьте)

Убедитесь что всё работает:

- [ ] SQLAlchemy установлен (`pip list | grep SQLAlchemy`)
- [ ] Тест БД прошел успешно (`python test_db_connection.py`)
- [ ] Бот запускается с "Database: Enabled ✅"
- [ ] Директория `data/` создана
- [ ] Файл `data/bot.db` существует
- [ ] Логи пишутся в `logs/bot.log`
- [ ] После теста заказа данные появились в БД

---

## 📚 Дополнительные ресурсы

### Файлы для изучения:
- `bot/models.py` - Модели БД и helper функции
- `bot/handlers/purchase.py` - Пример использования БД
- `bot/main.py` - Инициализация БД при старте
- `test_db_connection.py` - Тестовый скрипт

### Документация:
- SQLAlchemy: https://docs.sqlalchemy.org/
- SQLite: https://www.sqlite.org/docs.html

---

## 🎉 Готово!

Теперь ваш бот:
✅ Сохраняет все заказы в базу данных
✅ Ведет профили пользователей
✅ Собирает аналитику действий
✅ Логирует все события
✅ Готов к production использованию

**База данных подключена и работает!** 🚀

---

## 💡 Что дальше?

Теперь вы можете:
1. Добавить админ-панель для просмотра заказов
2. Создать отчеты по продажам
3. Настроить уведомления админу о новых заказах
4. Добавить систему промокодов
5. Интегрировать с платежными системами

Удачи! 🎯
