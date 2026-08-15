"""
Canary files - fake bait documents. If ANY of these are ever touched,
it's an instant, very high confidence ransomware signal (real programs
never touch them).
"""
import os
from app.settings import settings

CANARY_FILENAMES = ["salary.xlsx", "passwords.docx", "bank_statement.pdf", "employee_ssns.xlsx"]


def deploy_canary_files():
    """Creates the bait files if they don't already exist. Run this once at startup."""
    os.makedirs(settings.CANARY_DIR, exist_ok=True)
    created = []
    for filename in CANARY_FILENAMES:
        path = os.path.join(settings.CANARY_DIR, filename)
        if not os.path.exists(path):
            with open(path, "wb") as f:
                f.write(b"This is a decoy file used by RansomGuard for early ransomware detection.\n")
            created.append(path)
    return created


def is_canary_file(file_path: str) -> bool:
    return os.path.basename(file_path) in CANARY_FILENAMES
