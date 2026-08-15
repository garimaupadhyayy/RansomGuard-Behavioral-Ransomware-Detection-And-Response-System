"""
Maps our internal detection signal names to MITRE ATT&CK technique IDs.
"""

MITRE_TECHNIQUES = {
    "high_entropy":        ("T1486", "Data Encrypted for Impact"),
    "suspicious_extension": ("T1486", "Data Encrypted for Impact"),
    "mass_file_writes":     ("T1486", "Data Encrypted for Impact"),
    "rapid_rename":         ("T1486", "Data Encrypted for Impact"),
    "canary_triggered":     ("T1486", "Data Encrypted for Impact"),
    "unknown_process":      ("T1057", "Process Discovery"),
    "unsigned_binary":      ("T1105", "Ingress Tool Transfer"),
    "file_discovery":       ("T1083", "File and Directory Discovery"),
    "shadow_copy_deleted":  ("T1490", "Inhibit System Recovery"),
}


def map_signals_to_mitre(signal_names: list) -> list:
    """Given a list of triggered signal names, return unique (id, name) tuples."""
    seen = {}
    for signal in signal_names:
        if signal in MITRE_TECHNIQUES:
            tid, tname = MITRE_TECHNIQUES[signal]
            seen[tid] = tname
    return [{"id": tid, "name": name} for tid, name in seen.items()]
