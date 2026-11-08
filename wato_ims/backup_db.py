# backup_db.py
import os
import shutil
from datetime import datetime

DB_PATH = 'db.sqlite3'
BACKUP_DIR = 'backups'

def backup_database():
    if not os.path.exists(DB_PATH):
        print("Database file not found!")
        return

    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f'wato_ims_backup_{timestamp}.sqlite3'
    backup_filepath = os.path.join(BACKUP_DIR, backup_filename)

    shutil.copy(DB_PATH, backup_filepath)
    print(f"Successfully created backup: {backup_filepath}")

if __name__ == '__main__':
    backup_database()