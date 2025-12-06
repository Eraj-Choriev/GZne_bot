# 🚀 Настройка бота GZne_bot

## 📋 Шаг 1: Клонирование репозитория

```bash
git clone https://github.com/Eraj-Choriev/GZne_bot.git
cd GZne_bot
```

## 🔧 Шаг 2: Установка зависимостей

```bash
pip install -r requirements.txt
```

Если файла `requirements.txt` нет, установите необходимые пакеты:

```bash
pip install python-telegram-bot python-dotenv
```

## 🔑 Шаг 3: Настройка переменных окружения

1. Создайте файл `.env` из шаблона:
   ```bash
   cp .env.example .env
   ```

2. Откройте `.env` и заполните ваши данные:

   ```env
   # Получите токен у @BotFather в Telegram
   BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

   # Узнайте ваш ID у @userinfobot
   ADMIN_ID=123456789

   # Ваш username без @
   ADMIN_USERNAME=your_username
   ```

### 📝 Как получить токен бота:

1. Найдите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен в `.env`

### 🆔 Как узнать ваш Telegram ID:

1. Найдите [@userinfobot](https://t.me/userinfobot) в Telegram
2. Нажмите "Start" или отправьте любое сообщение
3. Бот пришлет ваш ID
4. Скопируйте ID в `.env`

## ▶️ Шаг 4: Запуск бота

```bash
python3 run.py
```

или

```bash
python run.py
```

Вы должны увидеть:
```
Bot is polling  let's fuckkk...
```

## ✅ Проверка работы

1. Найдите вашего бота в Telegram по username
2. Отправьте команду `/start`
3. Бот должен ответить приветственным сообщением

## 🧪 Тестирование базы данных

Проверьте работу базы данных продуктов:

```bash
python3 test_database.py
```

Вы должны увидеть:
```
✅ Products database loaded: 31 products
✅ ALL TESTS COMPLETED SUCCESSFULLY!
```

## 📁 Структура проекта

```
GZne_bot/
├── bot/
│   ├── __init__.py
│   ├── config.py          # Конфигурация бота
│   ├── data.py            # Утилиты для работы с данными
│   ├── database.py        # База данных продуктов
│   ├── keyboards.py       # Клавиатуры бота
│   ├── localization.py    # Мультиязычность
│   ├── main.py            # Основной файл бота
│   ├── payments.py        # Обработка платежей
│   ├── state.py           # Управление состоянием
│   └── handlers/          # Обработчики команд
│       ├── button.py
│       ├── errors.py
│       ├── language.py
│       ├── navigation.py
│       ├── purchase.py
│       ├── receipt.py
│       ├── start.py
│       ├── support.py
│       └── text.py
├── locales/
│   ├── products.json      # База данных товаров
│   ├── ru.json            # Русская локализация
│   └── tj.json            # Таджикская локализация
├── .env                   # Ваши секретные данные (НЕ коммитить!)
├── .env.example           # Пример конфигурации
├── run.py                 # Точка входа
├── test_database.py       # Тесты базы данных
├── DATABASE_USAGE.md      # Документация по БД
└── SETUP.md               # Эта инструкция
```

## ⚠️ Важно!

- **НИКОГДА** не коммитьте файл `.env` в Git!
- Файл `.env` уже добавлен в `.gitignore`
- Храните токен бота в секрете
- Не делитесь токеном с другими людьми

## 🐛 Решение проблем

### Бот не запускается

1. Проверьте, что `.env` файл существует:
   ```bash
   ls -la .env
   ```

2. Проверьте, что токен правильный:
   ```bash
   cat .env
   ```

3. Проверьте установлены ли зависимости:
   ```bash
   pip list | grep telegram
   ```

### База данных не загружается

1. Проверьте существует ли файл:
   ```bash
   ls -la locales/products.json
   ```

2. Запустите тесты:
   ```bash
   python3 test_database.py
   ```

## 📚 Дополнительная документация

- [DATABASE_USAGE.md](DATABASE_USAGE.md) - Работа с базой данных продуктов
- Документация python-telegram-bot: https://docs.python-telegram-bot.org/

## 🆘 Поддержка

Если у вас возникли проблемы:

1. Проверьте логи бота
2. Убедитесь что все зависимости установлены
3. Проверьте правильность токена и ID

---

**Готово! Ваш бот должен работать! 🎉**
