#!/bin/bash
# This script restores a specified backup of the SQLite database.

# Set variables
DATABASE_PATH="/home/ubuntu/CaC/Code-Against-Cancer/CodeAgainstCancer/db.sqlite3"
BACKUP_DIR="/home/ubuntu/CaC/backups"

# List available backups
echo "Available backups:"
ls -tp $BACKUP_DIR/db_backup_*.sqlite3

# Prompt for the backup file to restore
echo "Enter the name of the backup file you want to restore (e.g., db_backup_2024-11-12_02-54-01.sqlite3):"
read -r BACKUP_FILE_NAME

# Full path to the selected backup
BACKUP_FILE="$BACKUP_DIR/$BACKUP_FILE_NAME"

# Check if the selected backup file exists
if [ -f "$BACKUP_FILE" ]; then
    echo "Restoring backup from $BACKUP_FILE to $DATABASE_PATH..."
    
    # Copy the backup file to the database path
    cp "$BACKUP_FILE" "$DATABASE_PATH"
    
    echo "Database restored successfully from $BACKUP_FILE."
else
    echo "Error: Backup file $BACKUP_FILE does not exist."
fi
