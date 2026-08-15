"""
Phase 6 starter — weighted risk scoring engine.

This is the "brain" of RansomGuard. It takes a summary of what's been observed
recently (from the file watcher, process watcher, entropy checks, canary files)
and turns it into one risk score.

This is intentionally simple to start. As you build Phases 1-5, you'll feed real
data into this instead of the example dictionary below.
"""

from dataclasses import dataclass, field


WEIGHTS = {
    "rapid_rename": 20,
    "high_entropy": 30,
    "mass_file_writes": 20,
    "unknown_process": 10,
    "canary_triggered": 40,
    "unsigned_binary": 20,
}

RANSOMWARE_THRESHOLD = 80


@dataclass
class DetectionSignals:
    rapid_rename: bool = False
    high_entropy: bool = False
    mass_file_writes: bool = False
    unknown_process: bool = False
    canary_triggered: bool = False
    unsigned_binary: bool = False
    reasons: list = field(default_factory=list)


def calculate_risk_score(signals: DetectionSignals) -> dict:
    score = 0
    reasons = []

    for signal_name, weight in WEIGHTS.items():
        if getattr(signals, signal_name):
            score += weight
            reasons.append(f"{signal_name.replace('_', ' ')} (+{weight})")

    is_ransomware = score >= RANSOMWARE_THRESHOLD

    return {
        "score": score,
        "is_ransomware": is_ransomware,
        "reasons": reasons,
    }


if __name__ == "__main__":
    # Example: simulate a bad case to see the scoring engine work
    example = DetectionSignals(
        rapid_rename=True,
        high_entropy=True,
        canary_triggered=True,
    )
    result = calculate_risk_score(example)
    print(result)
