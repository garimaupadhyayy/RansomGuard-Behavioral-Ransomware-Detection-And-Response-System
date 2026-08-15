"""
Restore manager - copies the most recent clean backup back over a
damaged/encrypted file. This is the "auto recovery" step.
"""
import os
import shutil
from app.backup.backup_manager import find_latest_backup


def restore_file(damaged_path: str) -> dict:
    """Restores one file from the newest backup available. Returns a status dict."""
    filename = os.path.basename(damaged_path)
    backup_path = find_latest_backup(filename)

    if not backup_path:
        return {"restored": False, "reason": "No backup found for this file"}

    try:
        shutil.copy2(backup_path, damaged_path)
        return {"restored": True, "restored_from": backup_path}
    except OSError as e:
        return {"restored": False, "reason": str(e)}


def restore_multiple(damaged_paths: list) -> list:
    return [{"file": p, **restore_file(p)} for p in damaged_paths]
