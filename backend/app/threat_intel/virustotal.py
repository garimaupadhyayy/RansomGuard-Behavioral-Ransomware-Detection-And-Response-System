"""
VirusTotal integration - looks up a file's SHA-256 hash against
VirusTotal's database (70+ antivirus engines).

Get a free API key at: https://www.virustotal.com/gui/join-us
Free tier is rate-limited (4 requests/min) - fine for a learning project.
"""
import hashlib
import requests
from app.settings import settings

VT_BASE_URL = "https://www.virustotal.com/api/v3/files"


def calculate_sha256(file_path: str) -> str:
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def lookup_hash(sha256_hash: str) -> dict:
    """
    Looks up a hash on VirusTotal. Returns a simple dict:
        { "found": bool, "malicious_count": int, "total_engines": int, "flagged": bool }
    If no API key is set, or the hash isn't known to VT, returns found=False.
    """
    if not settings.VIRUSTOTAL_API_KEY:
        return {"found": False, "error": "No VIRUSTOTAL_API_KEY set in .env"}

    headers = {"x-apikey": settings.VIRUSTOTAL_API_KEY}
    try:
        resp = requests.get(f"{VT_BASE_URL}/{sha256_hash}", headers=headers, timeout=15)
    except requests.RequestException as e:
        return {"found": False, "error": str(e)}

    if resp.status_code == 404:
        return {"found": False, "malicious_count": 0, "total_engines": 0, "flagged": False}

    if resp.status_code != 200:
        return {"found": False, "error": f"VirusTotal returned status {resp.status_code}"}

    data = resp.json()
    stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
    malicious = stats.get("malicious", 0)
    total = sum(stats.values()) if stats else 0

    return {
        "found": True,
        "malicious_count": malicious,
        "total_engines": total,
        "flagged": malicious > 0,
    }


def scan_file_and_lookup(file_path: str) -> dict:
    """Convenience: hash a local file, then check it against VirusTotal."""
    sha256_hash = calculate_sha256(file_path)
    result = lookup_hash(sha256_hash)
    result["sha256"] = sha256_hash
    return result
