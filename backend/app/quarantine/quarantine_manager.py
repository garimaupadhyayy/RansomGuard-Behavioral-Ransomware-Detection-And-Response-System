"""
Quarantine manager - kills a malicious process and isolates its
executable so it can't run again.
"""
import os
import shutil
import datetime
import psutil
from app.settings import settings


def kill_process(pid: int) -> dict:
    """Terminates a process by PID. Escalates to kill() if it won't stop."""
    try:
        proc = psutil.Process(pid)
        exe_path = proc.exe()
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except psutil.TimeoutExpired:
            proc.kill()
        return {"killed": True, "pid": pid, "exe_path": exe_path}
    except psutil.NoSuchProcess:
        return {"killed": False, "reason": "Process already gone"}
    except psutil.AccessDenied:
        return {"killed": False, "reason": "Access denied (try running as admin)"}


def quarantine_file(file_path: str, reason: str = "") -> dict:
    """Moves a suspicious executable into an isolated quarantine folder."""
    if not os.path.exists(file_path):
        return {"quarantined": False, "reason": "File not found"}

    os.makedirs(settings.QUARANTINE_DIR, exist_ok=True)
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = os.path.basename(file_path)
    dest_path = os.path.join(settings.QUARANTINE_DIR, f"{timestamp}_{filename}")

    try:
        shutil.move(file_path, dest_path)
        return {"quarantined": True, "quarantine_path": dest_path, "reason": reason}
    except OSError as e:
        return {"quarantined": False, "reason": str(e)}


def contain_threat(pid: int, exe_path: str, reason: str = "High risk score") -> dict:
    """Full containment: kill the process, then quarantine its executable."""
    kill_result = kill_process(pid)
    quarantine_result = quarantine_file(exe_path, reason) if exe_path else {"quarantined": False}
    return {"kill": kill_result, "quarantine": quarantine_result}
