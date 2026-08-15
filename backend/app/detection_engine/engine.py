"""
The detection "brain" - combines every signal into one risk score,
maps it to MITRE, and decides whether to trigger a response.
"""
from dataclasses import dataclass, field
from app.mitre.mitre_map import map_signals_to_mitre

WEIGHTS = {
    "rapid_rename": 20,
    "high_entropy": 30,
    "mass_file_writes": 20,
    "unknown_process": 10,
    "canary_triggered": 40,
    "unsigned_binary": 20,
    "suspicious_extension": 25,
    "vt_flagged_malicious": 35,   # VirusTotal says this hash is known-bad
}

RANSOMWARE_THRESHOLD = 80
HIGH_SEVERITY_THRESHOLD = 50


@dataclass
class DetectionSignals:
    rapid_rename: bool = False
    high_entropy: bool = False
    mass_file_writes: bool = False
    unknown_process: bool = False
    canary_triggered: bool = False
    unsigned_binary: bool = False
    suspicious_extension: bool = False
    vt_flagged_malicious: bool = False


def severity_for_score(score: int) -> str:
    if score >= RANSOMWARE_THRESHOLD:
        return "critical"
    if score >= HIGH_SEVERITY_THRESHOLD:
        return "high"
    if score >= 20:
        return "medium"
    return "low"


def calculate_risk_score(signals: DetectionSignals) -> dict:
    score = 0
    triggered = []

    for signal_name, weight in WEIGHTS.items():
        if getattr(signals, signal_name, False):
            score += weight
            triggered.append(signal_name)

    is_ransomware = score >= RANSOMWARE_THRESHOLD
    mitre = map_signals_to_mitre(triggered)

    return {
        "score": score,
        "severity": severity_for_score(score),
        "is_ransomware": is_ransomware,
        "reasons": [f"{s.replace('_', ' ')} (+{WEIGHTS[s]})" for s in triggered],
        "mitre_techniques": mitre,
    }
