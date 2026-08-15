"""
YARA rule scanning - pattern matching for known ransomware indicators.

pip install yara-python
"""
import os
import yara

RULES_DIR = os.path.join(os.path.dirname(__file__), "rules")


def _compile_rules():
    rule_files = {}
    for filename in os.listdir(RULES_DIR):
        if filename.endswith(".yar") or filename.endswith(".yara"):
            name = filename.rsplit(".", 1)[0]
            rule_files[name] = os.path.join(RULES_DIR, filename)
    if not rule_files:
        return None
    return yara.compile(filepaths=rule_files)


_compiled = None


def get_compiled_rules():
    global _compiled
    if _compiled is None:
        _compiled = _compile_rules()
    return _compiled


def scan_file(file_path: str) -> list:
    """Returns a list of matched rule names, e.g. ['Suspicious_Ransom_Note_Text']."""
    rules = get_compiled_rules()
    if rules is None:
        return []
    try:
        matches = rules.match(file_path, timeout=10)
    except yara.Error:
        return []
    return [m.rule for m in matches]
