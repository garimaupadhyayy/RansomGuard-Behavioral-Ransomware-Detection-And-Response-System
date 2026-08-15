"""
All REST API routes.
"""
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional

from app.database.database import get_db
from app.models import models
from app.threat_intel.virustotal import lookup_hash
from app.reports.report_generator import generate_incident_report
from app.websocket.manager import manager
from app.auth.auth import create_access_token, verify_password, hash_password, get_current_user
from app.settings import settings

router = APIRouter()
CurrentUser = Depends(get_current_user)


# ---------- System status ----------
@router.get("/system/status")
def system_status():
    return {
        "simulation_mode": settings.SIMULATION_MODE,
        "watch_folders": settings.WATCH_FOLDERS,
        "virustotal_enabled": bool(settings.VIRUSTOTAL_API_KEY),
    }


# ---------- Events ----------
@router.get("/events/files")
def list_file_events(limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.FileEvent).order_by(models.FileEvent.timestamp.desc()).limit(limit).all()


@router.get("/events/processes")
def list_process_events(limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.ProcessEvent).order_by(models.ProcessEvent.timestamp.desc()).limit(limit).all()


# ---------- Alerts & Incidents ----------
@router.get("/alerts")
def list_alerts(limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.Alert).order_by(models.Alert.timestamp.desc()).limit(limit).all()


@router.get("/incidents")
def list_incidents(db: Session = Depends(get_db)):
    return db.query(models.Incident).order_by(models.Incident.started_at.desc()).all()


@router.get("/incidents/{incident_id}/report")
def download_incident_report(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(models.Incident).filter(models.Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(404, "Incident not found")
    alerts = db.query(models.Alert).filter(models.Alert.incident_id == incident_id).all()

    incident_dict = {c.name: getattr(incident, c.name) for c in incident.__table__.columns}
    alert_dicts = [{c.name: getattr(a, c.name) for c in a.__table__.columns} for a in alerts]

    path = generate_incident_report(incident_dict, alert_dicts)
    return {"report_path": path}


# ---------- Quarantine ----------
@router.get("/quarantine")
def list_quarantine(db: Session = Depends(get_db)):
    return db.query(models.QuarantineItem).order_by(models.QuarantineItem.timestamp.desc()).all()


# ---------- IOC Search (threat hunting) ----------
@router.get("/ioc/search")
def search_ioc(q: str, db: Session = Depends(get_db)):
    """Search hash / ip / domain / filename across stored IOCs and events."""
    ioc_matches = db.query(models.IOC).filter(models.IOC.value.contains(q)).all()
    file_matches = db.query(models.FileEvent).filter(models.FileEvent.file_path.contains(q)).limit(20).all()
    process_matches = db.query(models.ProcessEvent).filter(
        or_(models.ProcessEvent.sha256.contains(q), models.ProcessEvent.name.contains(q))
    ).limit(20).all()

    return {
        "iocs": ioc_matches,
        "file_events": file_matches,
        "process_events": process_matches,
    }


# ---------- Threat hunting ----------
@router.get("/hunt/unsigned-processes")
def hunt_unsigned(db: Session = Depends(get_db)):
    return db.query(models.ProcessEvent).filter(models.ProcessEvent.is_unknown == True).limit(100).all()  # noqa: E712


@router.get("/hunt/script-hosts")
def hunt_script_hosts(db: Session = Depends(get_db)):
    script_names = ["powershell.exe", "cmd.exe", "wscript.exe", "cscript.exe", "mshta.exe"]
    return db.query(models.ProcessEvent).filter(models.ProcessEvent.name.in_(script_names)).limit(100).all()


# ---------- VirusTotal manual lookup ----------
@router.get("/virustotal/lookup/{sha256_hash}")
def virustotal_lookup(sha256_hash: str):
    return lookup_hash(sha256_hash)


# ---------- MITRE matrix summary ----------
@router.get("/mitre/summary")
def mitre_summary(db: Session = Depends(get_db)):
    alerts = db.query(models.Alert).filter(models.Alert.mitre_techniques.isnot(None)).all()
    counts = {}
    for a in alerts:
        for tid in (a.mitre_techniques or "").split(","):
            tid = tid.strip()
            if tid:
                counts[tid] = counts.get(tid, 0) + 1
    return counts


# ---------- Auth ----------
@router.post("/auth/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.username == username).first()
    if existing:
        raise HTTPException(400, "Username already exists")
    user = models.User(username=username, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    return {"created": True, "username": username}


@router.post("/auth/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token({"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}


# ---------- WebSocket (live alert stream) ----------
@router.websocket("/ws/alerts")
async def websocket_alerts(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # keep connection open; client doesn't need to send anything meaningful
    except WebSocketDisconnect:
        manager.disconnect(websocket)
