#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <thu_muc>"
    exit 1
fi

SOURCE="$1"

if [ ! -d "$SOURCE" ]; then
    echo "Error: '$SOURCE' khong phai la thu muc."
    exit 2
fi

BACKUP_DIR="$HOME/backup"
mkdir -p "$BACKUP_DIR"

NAME=$(basename "$SOURCE")
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

BACKUP_FILE="$BACKUP_DIR/${NAME}_${TIMESTAMP}.tar.gz"

tar -czf "$BACKUP_FILE" -C "$(dirname "$SOURCE")" "$NAME"

echo "$(date '+%Y-%m-%d %H:%M:%S') $BACKUP_FILE" >> logs/backup.log

echo "Backup thanh cong: $BACKUP_FILE"

exit 0

