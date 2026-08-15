"""
Production process watcher - scans running processes, flags new/unknown ones,
optionally enriches with VirusTotal, and can trigger containment.

Run standalone with:
    python -m app.process_monitor.process_watcher
"""
import time
import hashlib
import psutil

from app.database.database import SessionLocal
from app.models.models import ProcessEvent
from app.threat_intel.virustotal import lookup_hash
from app.quarantine.quarantine_manager import contain_threat
from app.detection_engine.engine import DetectionSignals, calculate_risk_score
from app.settings import settings

_seen_pids = set()

KNOWN_SAFE_NAMES = {
    "explorer.exe", "svchost.exe", "chrome.exe", "firefox.exe", "code.exe",
    "python.exe", "python3", "systemd", "bash", "zsh", "Terminal",
}


def _hash_file(path: str) -> str:
    try:
        sha256 = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except (FileNotFoundError, PermissionError, OSError):
        return ""


def scan_processes(enrich_with_virustotal: bool = False):
    db = SessionLocal()
    try:
        for proc in psutil.process_iter(["pid", "ppid", "name", "exe", "cpu_percent", "memory_info"]):
            info = proc.info
            pid = info["pid"]
            if pid in _seen_pids:
                continue
            _seen_pids.add(pid)

            name = info.get("name") or "unknown"
            exe_path = info.get("exe") or ""
            is_unknown = name not in KNOWN_SAFE_NAMES

            sha256 = _hash_file(exe_path) if exe_path else ""
            vt_result = {"flagged": False}
            if enrich_with_virustotal and sha256:
                vt_result = lookup_hash(sha256)

            pe = ProcessEvent(
                pid=pid,
                parent_pid=info.get("ppid"),
                name=name,
                exe_path=exe_path,
                sha256=sha256 or None,
                cpu_percent=info.get("cpu_percent"),
                memory_mb=(info["memory_info"].rss / (1024 * 1024)) if info.get("memory_info") else None,
                is_unknown=is_unknown,
                vt_malicious_count=vt_result.get("malicious_count"),
                vt_checked=enrich_with_virustotal,
            )
            db.add(pe)
            db.commit()

            if is_unknown or vt_result.get("flagged"):
                print(f"[NEW PROCESS] pid={pid} name={name} unknown={is_unknown} vt_flagged={vt_result.get('flagged')}")

            signals = DetectionSignals(
                unknown_process=is_unknown,
                vt_flagged_malicious=vt_result.get("flagged", False),
            )
            result = calculate_risk_score(signals)

            if result["is_ransomware"]:
                if settings.SIMULATION_MODE:
                    print(f"[SIMULATION] Would contain: pid={pid} name={name} (no real action taken)")
                else:
                    print(f"[CONTAINMENT TRIGGERED] pid={pid} name={name}")
                    contain_threat(pid, exe_path, reason="High risk score from process behavior")

    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass
    finally:
        db.close()


if __name__ == "__main__":
    print("Starting process watcher (Ctrl+C to stop)...")
    while True:
        scan_processes(enrich_with_virustotal=False)  # set True once VT key is in .env
        time.sleep(3)
