"""
RansomGuard backend entry point.

Run it with:
    uvicorn app.main:app --reload
"""
import threading
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import init_db
from app.api.routes import router
from app.alerts.canary import deploy_canary_files
from app.process_monitor.file_watcher import start_watching
from app.process_monitor.process_watcher import scan_processes
from app.backup.scheduler import run_backup_loop
from app.settings import settings
import time

app = FastAPI(
    title="RansomGuard API",
    description="Real-time ransomware detection & auto-recovery system (educational project).",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ransomguard-backend"}


def _run_process_watcher_loop():
    while True:
        try:
            scan_processes(enrich_with_virustotal=True)
        except Exception as e:
            print(f"[process watcher error] {e}")
        time.sleep(3)


@app.on_event("startup")
def startup_event():
    init_db()
    deploy_canary_files()

    # Background thread: watch canary files + your real folders (set in .env WATCH_FOLDERS)
    watch_paths = [settings.CANARY_DIR] + settings.WATCH_FOLDERS
    watch_paths = [p for p in watch_paths if os.path.isdir(p)]
    if not watch_paths:
        print("[WARNING] No valid folders to watch. Check WATCH_FOLDERS in your .env file.")
    threading.Thread(target=start_watching, args=(watch_paths,), daemon=True).start()

    # Background thread: watch running processes
    threading.Thread(target=_run_process_watcher_loop, daemon=True).start()

    # Background thread: periodic backup of watched folders (so restore has something to use)
    if settings.WATCH_FOLDERS and settings.WATCH_FOLDERS != ["./test_folder"]:
        threading.Thread(target=run_backup_loop, daemon=True).start()

    mode = "SIMULATION MODE (safe - no real kill/quarantine/restore)" if settings.SIMULATION_MODE else "LIVE MODE (will actually kill/quarantine/restore)"
    print(f"RansomGuard backend started. Watchers running in background threads. Mode: {mode}")
