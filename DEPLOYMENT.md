# 🚀 Production Deployment Guide

Полное руководство по деплою GZne Bot в production.

---

## 📋 Содержание

1. [Требования](#требования)
2. [Подготовка сервера](#подготовка-сервера)
3. [Деплой с Docker](#деплой-с-docker)
4. [Деплой без Docker](#деплой-без-docker)
5. [Настройка мониторинга](#настройка-мониторинга)
6. [Бэкапы](#бэкапы)
7. [Обновления](#обновления)
8. [Troubleshooting](#troubleshooting)

---

## 🔧 Требования

### Минимальные требования к серверу:
- **CPU**: 1 core
- **RAM**: 512 MB (рекомендуется 1 GB)
- **Disk**: 2 GB свободного места
- **OS**: Linux (Ubuntu 20.04+, Debian 11+, CentOS 8+)

### Программное обеспечение:
- **Python**: 3.11+ (если без Docker)
- **Docker**: 20.10+ (если с Docker)
- **Docker Compose**: 2.0+ (если с Docker)

---

## 🖥️ Подготовка сервера

### 1. Обновление системы

```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y

# CentOS/RHEL
sudo yum update -y
```

### 2. Установка Docker (опционально)

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 3. Клонирование репозитория

```bash
cd /opt
sudo git clone https://github.com/Eraj-Choriev/GZne_bot.git
cd GZne_bot
```

---

## 🐳 Деплой с Docker (Рекомендуется)

### 1. Настройка окружения

```bash
# Скопируйте пример конфигурации
cp .env.example .env

# Отредактируйте .env
nano .env
```

Заполните обязательные переменные:
```env
BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_telegram_id
ADMIN_USERNAME=your_username

# Платежные данные
PAYMENT_DC_CARD=your_card_number
PAYMENT_ESKHATA_CARD=your_card_number
PAYMENT_ALIF_CARD=your_card_number
PAYMENT_VISA_CARD=your_card_number
```

### 2. Запуск бота

```bash
# Сборка и запуск
docker-compose up -d

# Проверка логов
docker-compose logs -f bot

# Проверка статуса
docker-compose ps
```

### 3. Полезные команды

```bash
# Остановка бота
docker-compose stop

# Перезапуск бота
docker-compose restart

# Просмотр логов последних 100 строк
docker-compose logs --tail=100 bot

# Вход в контейнер
docker-compose exec bot /bin/bash

# Обновление и перезапуск
git pull
docker-compose up -d --build
```

---

## 💻 Деплой без Docker

### 1. Установка Python 3.11+

```bash
# Ubuntu/Debian
sudo apt install -y python3.11 python3.11-venv python3-pip

# CentOS/RHEL
sudo yum install -y python311
```

### 2. Создание виртуального окружения

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Настройка .env

```bash
cp .env.example .env
nano .env
```

### 5. Запуск бота

**Способ 1: В фоне с nohup**
```bash
nohup python run.py > logs/bot.log 2>&1 &
```

**Способ 2: С systemd (рекомендуется)**

Создайте файл `/etc/systemd/system/gzne-bot.service`:

```ini
[Unit]
Description=GZne Telegram Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/opt/GZne_bot
Environment="PATH=/opt/GZne_bot/venv/bin"
ExecStart=/opt/GZne_bot/venv/bin/python /opt/GZne_bot/run.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Запустите сервис:

```bash
sudo systemctl daemon-reload
sudo systemctl enable gzne-bot
sudo systemctl start gzne-bot

# Проверка статуса
sudo systemctl status gzne-bot

# Просмотр логов
sudo journalctl -u gzne-bot -f
```

---

## 📊 Настройка мониторинга

### 1. Мониторинг через Sentry (опционально)

```bash
# Регистрация на sentry.io
# Получите DSN ключ

# Добавьте в .env
SENTRY_DSN=https://your-dsn@sentry.io/project-id
```

### 2. Health Check скрипт

Создайте `/opt/scripts/health_check.sh`:

```bash
#!/bin/bash
CONTAINER_NAME="gzne_bot"

if docker ps | grep -q $CONTAINER_NAME; then
    echo "✅ Bot is running"
    exit 0
else
    echo "❌ Bot is not running"
    # Попытка перезапуска
    docker-compose -f /opt/GZne_bot/docker-compose.yml up -d
    exit 1
fi
```

Добавьте в crontab для проверки каждые 5 минут:

```bash
crontab -e

# Добавьте строку:
*/5 * * * * /opt/scripts/health_check.sh >> /var/log/health_check.log 2>&1
```

---

## 💾 Бэкапы

### Автоматические бэкапы

```bash
# Ручной бэкап
./scripts/backup.sh

# Автоматические бэкапы (crontab)
crontab -e

# Каждый день в 3:00 утра
0 3 * * * cd /opt/GZne_bot && ./scripts/backup.sh >> /var/log/backup.log 2>&1

# Каждую неделю в воскресенье в 2:00
0 2 * * 0 cd /opt/GZne_bot && ./scripts/backup.sh >> /var/log/backup.log 2>&1
```

### Восстановление из бэкапа

```bash
# Список бэкапов
ls -lh backups/

# Восстановление
./scripts/restore.sh backups/gzne_bot_backup_20240101-030000.tar.gz

# Перезапуск бота
docker-compose restart
```

### Удаленное хранение бэкапов

```bash
# Отправка в S3 (AWS)
aws s3 cp backups/ s3://your-bucket/gzne-bot-backups/ --recursive

# Отправка по SCP
scp backups/gzne_bot_backup_*.tar.gz user@backup-server:/backups/

# Отправка в Google Drive (с rclone)
rclone copy backups/ gdrive:GZne_Bot_Backups/
```

---

## 🔄 Обновления

### Обновление с Docker

```bash
cd /opt/GZne_bot

# Остановка бота
docker-compose down

# Обновление кода
git pull

# Пересборка и запуск
docker-compose up -d --build

# Проверка логов
docker-compose logs -f bot
```

### Обновление без Docker

```bash
cd /opt/GZne_bot

# Остановка бота
sudo systemctl stop gzne-bot

# Обновление кода
git pull

# Обновление зависимостей
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Запуск бота
sudo systemctl start gzne-bot

# Проверка статуса
sudo systemctl status gzne-bot
```

---

## 🔍 Troubleshooting

### Бот не запускается

```bash
# Проверка логов (Docker)
docker-compose logs --tail=100 bot

# Проверка логов (systemd)
sudo journalctl -u gzne-bot -n 100

# Проверка конфигурации
cat .env | grep BOT_TOKEN
```

### Высокая нагрузка на CPU/RAM

```bash
# Проверка ресурсов (Docker)
docker stats gzne_bot

# Ограничение ресурсов в docker-compose.yml уже настроено

# Проверка процессов
top -p $(pgrep -f "python run.py")
```

### База данных повреждена

```bash
# Восстановление из бэкапа
./scripts/restore.sh backups/latest_backup.tar.gz

# Или пересоздание БД
rm data/bot.db
docker-compose restart
```

### Ошибки при отправке сообщений

```bash
# Проверка токена
curl https://api.telegram.org/bot${BOT_TOKEN}/getMe

# Проверка прав бота
# Убедитесь что бот не заблокирован
```

---

## 📈 Производительность

### Рекомендованные настройки

```env
# .env
LOG_LEVEL=INFO  # Не используйте DEBUG в production
RATE_LIMIT_PER_MINUTE=30  # Защита от спама
```

### Оптимизация базы данных

```bash
# Очистка старых событий аналитики (старше 90 дней)
sqlite3 data/bot.db "DELETE FROM analytics WHERE created_at < datetime('now', '-90 days');"

# Вакуум БД
sqlite3 data/bot.db "VACUUM;"
```

---

## 🔐 Безопасность

### Checklist безопасности:

- ✅ `.env` файл не в Git репозитории
- ✅ Файрвол настроен (UFW/iptables)
- ✅ SSH доступ только по ключу
- ✅ Регулярные обновления системы
- ✅ Автоматические бэкапы настроены
- ✅ Мониторинг логов включен
- ✅ Rate limiting активирован

### Настройка файрвола

```bash
# Ubuntu/Debian (UFW)
sudo ufw allow ssh
sudo ufw enable
sudo ufw status

# Только для webhook (если используется)
# sudo ufw allow 8443/tcp
```

---

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи: `docker-compose logs -f` или `journalctl -u gzne-bot -f`
2. Проверьте статус: `docker-compose ps` или `systemctl status gzne-bot`
3. Проверьте `.env` конфигурацию
4. Восстановите из бэкапа если необходимо

---

**Успешного деплоя! 🚀**
