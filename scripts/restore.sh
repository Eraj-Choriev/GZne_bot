#!/bin/bash
# Restore script for GZne Bot
# Usage: ./scripts/restore.sh <backup_file>

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if backup file is provided
if [ -z "$1" ]; then
    echo -e "${RED}❌ Error: No backup file specified${NC}"
    echo -e "${YELLOW}Usage: $0 <backup_file>${NC}"
    echo -e "${YELLOW}Available backups:${NC}"
    ls -lh backups/gzne_bot_backup_*.tar.gz 2>/dev/null || echo "No backups found"
    exit 1
fi

BACKUP_FILE="$1"

# Check if backup file exists
if [ ! -f "$BACKUP_FILE" ]; then
    echo -e "${RED}❌ Error: Backup file not found: $BACKUP_FILE${NC}"
    exit 1
fi

echo -e "${YELLOW}⚠️  WARNING: This will overwrite current data!${NC}"
echo -e "${YELLOW}Backup file: $BACKUP_FILE${NC}"
read -p "Are you sure you want to continue? (yes/no): " -r
echo

if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
    echo -e "${BLUE}❌ Restore cancelled${NC}"
    exit 0
fi

# Create backup of current data before restoring
echo -e "${BLUE}📦 Creating safety backup of current data...${NC}"
./scripts/backup.sh

# Extract backup
echo -e "${BLUE}📂 Extracting backup...${NC}"
tar -xzf "$BACKUP_FILE"

echo -e "${GREEN}✅ Restore completed successfully!${NC}"
echo -e "${GREEN}Please restart the bot for changes to take effect.${NC}"
