# 📚 Документация по использованию базы данных продуктов

## ✅ Что было исправлено

1. **Очищен `products.json`** от ошибок `:contentReference`
2. **Создана структурированная база данных** с мультиязычной поддержкой (RU/TJ)
3. **Разработан модуль `database.py`** для удобной работы с продуктами
4. **Обновлен `data.py`** с полной обратной совместимостью
5. **Все тесты пройдены** — 31 товар в 5 категориях

---

## 📊 Структура базы данных

### Категории товаров:
- **🎮 Игры и игровые сервисы** (`games`) — 6 товаров
- **💰 Игровые ценности** (`currency`) — 7 товаров
- **📱 Мобильные игры** (`mobile`) — 5 товаров
- **⭐ Сервисы и соцсети** (`services`) — 6 товаров
- **💻 Программы** (`software`) — 7 товаров

### Формат продукта в JSON:
```json
{
  "id": "chatgpt_plus",
  "name": {
    "ru": "ChatGPT Plus 5.1 — 1 месяц",
    "tj": "ChatGPT Plus 5.1 — 1 моҳ"
  },
  "price_usd": 27.17,
  "price_tjs": 288.00,
  "type": {
    "ru": "Подписка",
    "tj": "Обуна"
  },
  "platform": "ChatGPT",
  "delivery": {
    "ru": "После оплаты",
    "tj": "Баъд аз пардохт"
  },
  "description": {
    "ru": "Описание на русском",
    "tj": "Тавсиф ба тоҷикӣ"
  },
  "icon": "🤖",
  "popular": true,
  "discount": null,
  "validity": {
    "ru": "1 месяц",
    "tj": "1 моҳ"
  }
}
```

---

## 🚀 Как использовать новую базу данных

### 1️⃣ Импорт модулей

```python
from bot.database import get_database, get_product_by_id, get_products_by_category
from bot.data import find_product, get_all_categories
```

### 2️⃣ Получить все категории

```python
# На русском
categories_ru = get_all_categories('ru')
# {'games': '🎮 Игры и игровые сервисы', ...}

# На таджикском
categories_tj = get_all_categories('tj')
# {'games': '🎮 Бозиҳо ва хидматҳои бозӣ', ...}
```

### 3️⃣ Получить товары из категории

```python
# Все игры на русском
games = get_products_by_category('games', 'ru')

for product in games:
    print(product['name'])  # Уже локализовано!
    print(product['price_tjs'])
```

### 4️⃣ Найти товар по ID

```python
# Найти продукт
product = find_product('chatgpt_plus', 'ru')

if product:
    print(product['name'])  # "ChatGPT Plus 5.1 — 1 месяц"
    print(product['price_tjs'])  # 288.00
```

### 5️⃣ Поиск товаров

```python
db = get_database()

# Поиск по тексту
results = db.search_products('ChatGPT', 'ru')
print(f"Найдено: {len(results)} товаров")
```

### 6️⃣ Популярные товары

```python
db = get_database()

# Топ-10 популярных товаров
popular = db.get_popular_products('ru', limit=10)

for product in popular:
    print(f"{product['name']} - {product['price_tjs']} TJS")
```

### 7️⃣ Форматирование для отображения

```python
db = get_database()

# Красивое имя с иконками
display_name = db.get_product_display_name(product)
# "🤖 ChatGPT Plus 5.1 — 1 месяц 🔥"

# Форматированная цена
price = db.format_price(product, 'TJS')
# "💵 288.00 TJS"

# Полное описание
details = db.get_product_details(product, 'ru')
print(details)
```

### 8️⃣ Обратная совместимость

Старый код продолжает работать без изменений:

```python
from bot.data import PRODUCTS

# Старый способ (все еще работает!)
products = PRODUCTS['ru']['cat_games']
```

---

## 🧪 Тестирование

Запустите тест для проверки работы:

```bash
python3 test_database.py
```

Результат:
```
✅ Products database loaded: 31 products
✅ Test 1: Database Loading
✅ Test 2: Categories (Russian)
✅ Test 3: Categories (Tajik)
...
✅ ALL TESTS COMPLETED SUCCESSFULLY!
```

---

## 📝 Примеры использования в боте

### Пример 1: Показать категории пользователю

```python
from bot.database import get_database

def show_categories(lang='ru'):
    db = get_database()
    categories = db.get_categories(lang)

    for cat_id, cat_name in categories.items():
        icon = db.get_category_icon(cat_id)
        products_count = len(db.get_products_by_category(cat_id, lang))
        print(f"{cat_name}: {products_count} товаров")
```

### Пример 2: Показать товары категории

```python
from bot.database import get_database

def show_products(category_id, lang='ru'):
    db = get_database()
    products = db.get_products_by_category(category_id, lang)

    for product in products:
        name = db.get_product_display_name(product)
        price = db.format_price(product, 'TJS')
        print(f"{name}\n{price}\n")
```

### Пример 3: Детали товара

```python
from bot.database import get_database

def show_product_details(product_id, lang='ru'):
    db = get_database()
    product = db.get_product_by_id(product_id, lang)

    if product:
        details = db.get_product_details(product, lang)
        return details
    else:
        return "Товар не найден"
```

---

## 🔧 API Reference

### `ProductDatabase` класс

| Метод | Описание |
|-------|----------|
| `load()` | Загрузить базу данных из JSON |
| `get_categories(lang)` | Получить все категории |
| `get_category_icon(category_id)` | Получить иконку категории |
| `get_products_by_category(category_id, lang)` | Получить товары категории |
| `get_product_by_id(product_id, lang)` | Найти товар по ID |
| `search_products(query, lang)` | Поиск товаров по тексту |
| `get_popular_products(lang, limit)` | Получить популярные товары |
| `get_total_products()` | Общее количество товаров |
| `get_product_display_name(product)` | Форматированное имя товара |
| `format_price(product, currency)` | Форматированная цена |
| `get_product_details(product, lang)` | Полное описание товара |

### Convenience функции в `data.py`

```python
from bot.data import (
    get_all_categories,        # Получить категории
    find_product,              # Найти товар по ID
    get_product_display_name,  # Форматированное имя
    get_product_price,         # Форматированная цена
    get_product_details,       # Полное описание
)
```

---

## ✨ Преимущества новой системы

1. **Чисто и структурировано** — данные в JSON, логика в Python
2. **Мультиязычность** — поддержка русского и таджикского из коробки
3. **Легко расширять** — просто добавьте товар в JSON
4. **Быстрый поиск** — поиск по ID, категории, тексту
5. **Форматирование** — встроенные функции для красивого отображения
6. **Обратная совместимость** — старый код работает без изменений
7. **Протестировано** — все функции покрыты тестами

---

## 📦 Добавление нового товара

1. Откройте `locales/products.json`
2. Найдите нужную категорию в `products`
3. Добавьте новый объект товара:

```json
{
  "id": "new_product_id",
  "name": {
    "ru": "Название на русском",
    "tj": "Номгузорӣ ба тоҷикӣ"
  },
  "price_usd": 10.00,
  "price_tjs": 106.00,
  "type": {
    "ru": "Тип",
    "tj": "Навъ"
  },
  "platform": "Платформа",
  "delivery": {
    "ru": "Способ доставки",
    "tj": "Тарзи расонидан"
  },
  "description": {
    "ru": "Описание",
    "tj": "Тавсиф"
  },
  "icon": "🎮",
  "popular": false,
  "discount": null,
  "validity": {
    "ru": "Срок действия",
    "tj": "Муддати амал"
  }
}
```

4. Сохраните файл
5. База данных автоматически обновится при следующей загрузке!

---

## 🎯 Итоги

✅ **31 товар** загружено в базу данных
✅ **5 категорий** работают корректно
✅ **2 языка** (русский и таджикский)
✅ **Все тесты пройдены** успешно
✅ **Чистый код** и понятная структура
✅ **Готово к использованию** в боте

---

**Создано с ❤️ для чистого и структурированного кода**
