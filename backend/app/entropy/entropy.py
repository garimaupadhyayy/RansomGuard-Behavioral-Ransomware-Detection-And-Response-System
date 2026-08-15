"""
Entropy calculation - detects encrypted-looking file content.
"""
import math
from collections import Counter

ENTROPY_THRESHOLD = 7.5

def calculate_entropy(file_path: str) -> float:
    try:
        with open(file_path, "rb") as f:
            data = f.read()
    except (FileNotFoundError, PermissionError, IsADirectoryError):
        return 0.0

    if not data:
        return 0.0

    counts = Counter(data)
    total = len(data)
    entropy = 0.0
    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)
    return round(entropy, 3)


def is_high_entropy(file_path: str) -> bool:
    return calculate_entropy(file_path) >= ENTROPY_THRESHOLD


SUSPICIOUS_EXTENSIONS = {
    ".locked", ".crypt", ".enc", ".encrypted", ".ransom", ".crypted",
    ".locky", ".cerber", ".zzz", ".xxx", ".micro", ".r5a", ".ecc",
}

def has_suspicious_extension(file_path: str) -> bool:
    lower = file_path.lower()
    return any(lower.endswith(ext) for ext in SUSPICIOUS_EXTENSIONS)
