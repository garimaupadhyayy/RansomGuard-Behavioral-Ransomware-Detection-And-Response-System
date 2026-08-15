"""
Central app settings, loaded from .env
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://ransomguard:ransomguard_dev_password@localhost:3306/ransomguard")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev_secret_change_me")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY", "")
    SMTP_HOST = os.getenv("SMTP_HOST", "")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    ALERT_EMAIL_TO = os.getenv("ALERT_EMAIL_TO", "")

    BACKUP_DIR = os.getenv("BACKUP_DIR", "./backups")
    QUARANTINE_DIR = os.getenv("QUARANTINE_DIR", "./quarantine_storage")
    CANARY_DIR = os.getenv("CANARY_DIR", "./canary_files")

    # Comma-separated list of real folders to monitor, e.g.:
    # WATCH_FOLDERS=C:\Users\indre\Desktop,C:\Users\indre\Documents,C:\Users\indre\Downloads
    WATCH_FOLDERS = [p.strip() for p in os.getenv("WATCH_FOLDERS", "./test_folder").split(",") if p.strip()]

    # SIMULATION_MODE=true (default, SAFE): detects and alerts, but never actually
    # kills a process, quarantines a file, or restores anything. Set to "false"
    # only once you trust the detection engine on your real folders.
    SIMULATION_MODE = os.getenv("SIMULATION_MODE", "true").lower() == "true"

    # How often (in seconds) to auto-backup the watched folders. Default: every 5 minutes.
    BACKUP_INTERVAL_SECONDS = int(os.getenv("BACKUP_INTERVAL_SECONDS", "300"))

settings = Settings()
