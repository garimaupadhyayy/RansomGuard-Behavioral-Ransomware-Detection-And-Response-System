"""
Phase 4 starter — entropy calculation.

Entropy is a number from 0 to 8 that measures how "random" the bytes in a file look.
- Plain text, spreadsheets, normal documents: usually low-to-medium entropy (~2-6).
- Encrypted or compressed files: very high entropy (~7.5-8).

This is one of the strongest signals that a file has been encrypted by ransomware.

Try it:
1. Run this on a normal .txt file -> expect a lower number.
2. Run this on a .zip file (zip files are already "compressed", similar to encrypted) ->
   expect a high number, close to 8.
3. Compare the two.
"""

import math
import sys
from collections import Counter


def calculate_entropy(file_path: str) -> float:
    with open(file_path, "rb") as f:
        data = f.read()

    if not data:
        return 0.0

    counts = Counter(data)
    total = len(data)
    entropy = 0.0
    for count in counts.values():
        probability = count / total
        entropy -= probability * math.log2(probability)

    return round(entropy, 3)


def is_suspiciously_encrypted(entropy_value: float, threshold: float = 7.5) -> bool:
    return entropy_value >= threshold


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python entropy_starter.py /path/to/file")
        sys.exit(1)

    path = sys.argv[1]
    score = calculate_entropy(path)
    flagged = is_suspiciously_encrypted(score)
    print(f"File: {path}")
    print(f"Entropy: {score} / 8.0")
    print(f"Looks encrypted: {'YES - suspicious' if flagged else 'no'}")
