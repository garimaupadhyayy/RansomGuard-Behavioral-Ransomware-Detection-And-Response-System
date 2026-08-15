"""
Backup manager - keeps timestamped copies of watched folders so we always
have something clean to restore from.
"""
import os
import shutil
import datetime
from app.settings import settings


def backup_file(source_path: str) -> str:
    """Copies a single file into a timestamped backup folder. Returns the backup path."""
    if not os.path.exists(source_path):
        return ""

    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = os.path.basename(source_path)
    dest_dir = os.path.join(settings.BACKUP_DIR, timestamp)
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, filename)
    shutil.copy2(source_path, dest_path)
    return dest_path


def backup_folder(folder_path: str) -> str:
    """Copies an entire folder into a timestamped backup. Returns the backup folder path."""
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    folder_name = os.path.basename(folder_path.rstrip("/\\"))
    dest_dir = os.path.join(settings.BACKUP_DIR, f"{folder_name}_{timestamp}")

    ignore = shutil.ignore_patterns(
        ".git", "node_modules", "venv", "__pycache__",
        "backups", "quarantine_storage", "reports_output", "*.pyc",
    )
    shutil.copytree(folder_path, dest_dir, dirs_exist_ok=True, ignore=ignore)
    return dest_dir


def find_latest_backup(filename: str) -> str:
    """Searches backup folders (newest first) for the most recent copy of a filename."""
    if not os.path.isdir(settings.BACKUP_DIR):
        return ""
    candidates = []
    for root, _, files in os.walk(settings.BACKUP_DIR):
        if filename in files:
            candidates.append(os.path.join(root, filename))
    if not candidates:
        return ""
    candidates.sort(key=os.path.getmtime, reverse=True)
    return candidates[0]
