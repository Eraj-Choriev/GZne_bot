#!/bin/bash
# Automatic backup script for GZne Bot
# Usage: ./scripts/backup.sh

set -e

# Configuration
BACKUP_DIR="./backups"
DATA_DIR="./data"
LOCALES_DIR="./locales"
DATE=$(date +%Y%m%d-%H%M%S)
BACKUP_NAME="gzne_bot_backup_${DATE}.tar.gz"
KEEP_DAYS=30

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔄 Starting backup...${NC}"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Create backup
echo -e "${BLUE}📦 Creating backup archive...${NC}"
tar -czf "${BACKUP_DIR}/${BACKUP_NAME}" \
    "$DATA_DIR" \
    "$LOCALES_DIR" \
    --exclude="*.pyc" \
    --exclude="__pycache__"

# Check if backup was created successfully
if [ -f "${BACKUP_DIR}/${BACKUP_NAME}" ]; then
    SIZE=$(du -h "${BACKUP_DIR}/${BACKUP_NAME}" | cut -f1)
    echo -e "${GREEN}✅ Backup created successfully!${NC}"
    echo -e "${GREEN}   File: ${BACKUP_NAME}${NC}"
    echo -e "${GREEN}   Size: ${SIZE}${NC}"
else
    echo -e "${RED}❌ Backup failed!${NC}"
    exit 1
fi

# Clean old backups
echo -e "${BLUE}🧹 Cleaning old backups (older than ${KEEP_DAYS} days)...${NC}"
find "$BACKUP_DIR" -name "gzne_bot_backup_*.tar.gz" -mtime +${KEEP_DAYS} -delete

# Show remaining backups
BACKUP_COUNT=$(find "$BACKUP_DIR" -name "gzne_bot_backup_*.tar.gz" | wc -l)
echo -e "${GREEN}📊 Total backups: ${BACKUP_COUNT}${NC}"

echo -e "${GREEN}✨ Backup completed!${NC}"
