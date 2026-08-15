"""
All database tables (MySQL) live here as SQLAlchemy models.
"""
import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="analyst")  # admin / analyst
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class FileEvent(Base):
    __tablename__ = "file_events"
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(50))       # created / modified / deleted / renamed
    file_path = Column(String(1024))
    dest_path = Column(String(1024), nullable=True)  # used for renames
    entropy = Column(Float, nullable=True)
    is_canary = Column(Boolean, default=False)
    suspicious_extension = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)


class ProcessEvent(Base):
    __tablename__ = "process_events"
    id = Column(Integer, primary_key=True, index=True)
    pid = Column(Integer)
    parent_pid = Column(Integer, nullable=True)
    name = Column(String(255))
    exe_path = Column(String(1024), nullable=True)
    sha256 = Column(String(64), nullable=True, index=True)
    cpu_percent = Column(Float, nullable=True)
    memory_mb = Column(Float, nullable=True)
    is_signed = Column(Boolean, nullable=True)
    is_unknown = Column(Boolean, default=False)
    vt_malicious_count = Column(Integer, nullable=True)  # VirusTotal enrichment
    vt_checked = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)


class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=True)
    score = Column(Integer)
    reasons = Column(Text)          # comma separated reasons
    mitre_techniques = Column(Text) # comma separated technique IDs
    severity = Column(String(20))   # low / medium / high / critical
    process_name = Column(String(255), nullable=True)
    file_path = Column(String(1024), nullable=True)
    is_ransomware = Column(Boolean, default=False)
    action_taken = Column(String(255), nullable=True)  # e.g. "process killed, files restored"
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    incident = relationship("Incident", back_populates="alerts")


class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    hostname = Column(String(255), nullable=True)
    user = Column(String(255), nullable=True)
    status = Column(String(50), default="open")  # open / contained / recovered / closed
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    alerts = relationship("Alert", back_populates="incident")


class QuarantineItem(Base):
    __tablename__ = "quarantine_items"
    id = Column(Integer, primary_key=True, index=True)
    original_path = Column(String(1024))
    quarantine_path = Column(String(1024))
    sha256 = Column(String(64), nullable=True)
    reason = Column(String(255), nullable=True)
    process_killed_pid = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)


class IOC(Base):
    """Indicators of Compromise - searchable hashes/IPs/domains/filenames."""
    __tablename__ = "iocs"
    id = Column(Integer, primary_key=True, index=True)
    ioc_type = Column(String(50))   # hash / ip / domain / filename
    value = Column(String(512), index=True)
    source = Column(String(100), nullable=True)  # e.g. "virustotal", "manual", "yara"
    notes = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
