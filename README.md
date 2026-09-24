<div align="center">

# RansomGuard

**Behavioral Ransomware Detection, Containment & Automated Recovery Platform**

![alt text](<Screenshot 2026-08-15 231058-2.png>)

</div>

## Overview

RansomGuard is a self-hosted, local-first EDR (Endpoint Detection & Response) system designed to detect ransomware through **behavioral analysis** rather than signature matching.

It continuously monitors file-system and process activity, evaluates multiple security signals through a weighted detection engine, maps confirmed threats to MITRE ATT&CK techniques, and supports automated containment, quarantine, and file recovery. Detection and response activity is presented through a real-time SOC-style dashboard.

This is an educational, defensive-security project. It contains no exploit code, malware, or offensive tooling. Testing is performed using simulated ransomware behavior such as rapid file renaming and high-entropy writes inside an isolated environment.

**Runs entirely on your own machine.** There is no hosted or cloud version.

<br>

## Why This Project

RansomGuard is designed to demonstrate a complete endpoint security workflow rather than a one-time security scan.

It demonstrates:

- **Behavioral detection engineering** using weighted, multi-signal scoring
- **End-to-end incident response** from detection to containment and recovery
- **Threat intelligence integration** through VirusTotal hash reputation and YARA rules
- **MITRE ATT&CK mapping** for detected security activity
- **SOC-style monitoring** through a real-time WebSocket dashboard

<br>

## Key Highlights

- Real-time file and process monitoring
- Behavioral ransomware detection
- Weighted risk scoring with **80+** confirmation threshold
- **70+ antivirus engines** through VirusTotal hash reputation
- **5 MITRE ATT&CK techniques** mapped to detected threats
- Entropy, YARA, canary-file and hash-based detection
- Automated process containment and quarantine
- Scheduled backup and file recovery
- IOC search and threat-hunting capabilities
- Real-time SOC dashboard
- PDF incident reporting
- Safe Simulation Mode

<br>

## Features

| Category | Capability |
|---|---|
| File monitoring | Real-time create/modify/rename/delete tracking via `watchdog` |
| Process monitoring | Tracks running processes using `psutil` |
| Entropy detection | Flags encrypted-looking content using Shannon entropy |
| Canary files | Uses decoy documents as high-confidence ransomware indicators |
| Weighted risk engine | Combines multiple signals into a single risk score |
| MITRE ATT&CK mapping | Maps detected behavior to ATT&CK techniques |
| VirusTotal integration | SHA-256 hash reputation across 70+ antivirus engines |
| YARA scanning | Pattern-based detection for ransomware-related behavior |
| Backup & recovery | Scheduled snapshots and recovery of monitored files |
| Process containment | Contains suspicious processes |
| Quarantine | Isolates suspicious executables |
| IOC search | Searches hashes, filenames and paths |
| Threat hunting | Searches suspicious processes and script-host activity |
| PDF reports | Generates incident reports |
| Live dashboard | Real-time alerts, timeline and MITRE visibility |
| Simulation Mode | Detects and alerts without performing real response actions |

<br>

## Detection & Risk Assessment

RansomGuard combines multiple behavioral indicators instead of depending on a single signature.

```text
File / Process Activity
          ↓
   Signal Extraction
          ↓
 ┌─────────────────────┐
 │ Entropy Analysis    │
 │ Canary File Hits    │
 │ File Behavior       │
 │ Process Behavior    │
 │ YARA Detection      │
 │ Hash Reputation     │
 └──────────┬──────────┘
            ↓
     Weighted Risk Score
            ↓
     Score ≥ 80
            ↓
    Confirmed Incident
