"""
Scheduled backup - periodically snapshots every watched folder so that
restore_file() actually has something recent to recover from.

Runs as a background thread, started from main.py on startup.
"""
import time
from app.backup.backup_manager import backup_folder
from app.settings import settings


def run_backup_loop():
    while True:
        for folder in settings.WATCH_FOLDERS:
            try:
                backup_folder(folder)
                print(f"[backup] snapshot taken of {folder}")
            except (OSError, FileNotFoundError) as e:
                print(f"[backup] skipped {folder}: {e}")
        time.sleep(settings.BACKUP_INTERVAL_SECONDS)
