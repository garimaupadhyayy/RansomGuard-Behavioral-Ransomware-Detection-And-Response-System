"""
Production file watcher - watches folders, scores events, triggers response.

Run standalone with:
    python -m app.process_monitor.file_watcher /path/to/folder1 /path/to/folder2
"""
import sys
import time
import collections
from datetime import datetime, timedelta
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import socket
import getpass
from app.database.database import SessionLocal
from app.models.models import FileEvent, Alert, Incident
from app.entropy.entropy import calculate_entropy, is_high_entropy, has_suspicious_extension
from app.alerts.canary import is_canary_file
from app.detection_engine.engine import DetectionSignals, calculate_risk_score
from app.restore.restore_manager import restore_file
from app.alerts.email_alert import send_alert_email
from app.yara_rules.yara_scanner import scan_file
from app.settings import settings

# Paths matching these substrings are ignored - they're RansomGuard's own
# internal files (backups, quarantine, git repos, dependency folders), not
# real user activity. Without this, watching your own project folder
# (e.g. Desktop) creates an infinite noise loop with its own backup snapshots.
IGNORED_PATH_MARKERS = [
    "\\backups\\", "/backups/",
    "\\quarantine_storage\\", "/quarantine_storage/",
    "\\.git\\", "/.git/",
    "\\node_modules\\", "/node_modules/",
    "\\venv\\", "/venv/",
    "\\__pycache__\\", "/__pycache__/",
    "\\reports_output\\", "/reports_output/",
]


def _is_ignored(path: str) -> bool:
    return any(marker in path for marker in IGNORED_PATH_MARKERS)

# Tracks recent rename/write counts per rolling 10-second window to catch "mass" activity
_recent_events = collections.deque(maxlen=200)


def _recent_event_count(seconds=10) -> int:
    cutoff = datetime.utcnow() - timedelta(seconds=seconds)
    return sum(1 for t in _recent_events if t >= cutoff)


class RansomGuardHandler(FileSystemEventHandler):
    def _record(self, event_type, src_path, dest_path=None):
        if _is_ignored(src_path) or (dest_path and _is_ignored(dest_path)):
            return

        _recent_events.append(datetime.utcnow())

        entropy_value = calculate_entropy(src_path) if event_type in ("modified", "created") else None
        high_entropy = entropy_value is not None and entropy_value >= 7.5
        canary_hit = is_canary_file(src_path)
        suspicious_ext = has_suspicious_extension(src_path)
        mass_writes = _recent_event_count() >= 15
        yara_matches = scan_file(src_path) if event_type in ("modified", "created") else []

        db = SessionLocal()
        try:
            fe = FileEvent(
                event_type=event_type,
                file_path=src_path,
                dest_path=dest_path,
                entropy=entropy_value,
                is_canary=canary_hit,
                suspicious_extension=suspicious_ext,
            )
            db.add(fe)
            db.commit()

            signals = DetectionSignals(
                rapid_rename=(event_type == "moved" and _recent_event_count(5) >= 5),
                high_entropy=high_entropy,
                mass_file_writes=mass_writes,
                canary_triggered=canary_hit,
                suspicious_extension=suspicious_ext,
            )
            result = calculate_risk_score(signals)

            if yara_matches:
                result["reasons"].append(f"YARA match: {', '.join(yara_matches)}")

            print(f"[{event_type.upper()}] {src_path} | score={result['score']} severity={result['severity']}")

            if result["score"] >= 20:  # log any meaningful signal as an alert
                action = "none"
                incident_id = None

                if result["is_ransomware"]:
                    if settings.SIMULATION_MODE:
                        action = "SIMULATION MODE: would have attempted restore (no real action taken)"
                        print(f"[SIMULATION] Would restore: {src_path}")
                    else:
                        restore_result = restore_file(src_path)
                        action = f"restore_attempted: {restore_result}"

                    send_alert_email(
                        subject=f"RANSOMWARE DETECTED - score {result['score']}",
                        body=f"File: {src_path}\nReasons: {result['reasons']}\nAction: {action}",
                    )

                    # Create an incident record so it shows up in the dashboard + PDF report
                    incident = Incident(
                        title=f"Ransomware activity detected on {src_path}",
                        hostname=socket.gethostname(),
                        user=getpass.getuser(),
                        status="simulated" if settings.SIMULATION_MODE else "contained",
                    )
                    db.add(incident)
                    db.commit()
                    db.refresh(incident)
                    incident_id = incident.id

                alert = Alert(
                    incident_id=incident_id,
                    score=result["score"],
                    reasons=", ".join(result["reasons"]),
                    mitre_techniques=", ".join(t["id"] for t in result["mitre_techniques"]),
                    severity=result["severity"],
                    file_path=src_path,
                    is_ransomware=result["is_ransomware"],
                    action_taken=action,
                )
                db.add(alert)
                db.commit()
        finally:
            db.close()

    def on_created(self, event):
        if not event.is_directory:
            self._record("created", event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self._record("modified", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self._record("deleted", event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            self._record("moved", event.src_path, dest_path=event.dest_path)


def start_watching(paths: list):
    observer = Observer()
    handler = RansomGuardHandler()
    for path in paths:
        observer.schedule(handler, path, recursive=True)
        print(f"Watching: {path}")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    watch_paths = sys.argv[1:] or ["./test_folder"]
    start_watching(watch_paths)
