#!/bin/bash
# This script creates a backup of the SQLite database and keeps only the two most recent backups.
# The script is intended to be run as a cron job.
# The script should be run in the EC2 instance where the database is located.

# Set variables
TIMESTAMP=$(date +'%Y-%m-%d_%H-%M-%S')
DATABASE_PATH="/home/ubuntu/CaC/data/db.sqlite3"
BACKUP_DIR="/home/ubuntu/CaC/backups"
BACKUP_FILE="$BACKUP_DIR/db_backup_$TIMESTAMP.sqlite3"

# Create the backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Using SQLite's .backup command to create a safe copy
sqlite3 "$DATABASE_PATH" ".backup '$BACKUP_FILE'"
echo "Database backup created at $BACKUP_FILE"

# Keep only the last five backups [+3 to skip the first two lines of ls output]
ls -tp $BACKUP_DIR/db_backup_*.sqlite3 | tail -n +3 | xargs -I {} rm -- {}
echo "Old backups cleaned up, retaining only the five most recent files."
