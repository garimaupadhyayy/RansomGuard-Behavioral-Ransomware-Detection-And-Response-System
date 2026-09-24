<div align="center">

# RansomGuard

**Behavioral Ransomware Detection, Containment & Automated Recovery Platform**

![alt text](<Screenshot 2026-08-15 231058-2.png>)

</div>

## Overview

RansomGuard is a self-hosted, local-first EDR (Endpoint Detection & Response) system designed to protect files and endpoint activity from ransomware through **behavioral analysis** rather than signature matching.

The system continuously monitors file-system and process activity, evaluates multiple security signals through a weighted risk engine, maps confirmed threats to MITRE ATT&CK techniques, and supports automated containment, quarantine, and file recovery. All detection and response activity is presented through a real-time SOC-style dashboard.

RansomGuard is designed as an educational defensive-security project and operates entirely on the local machine. It uses simulated ransomware behavior in an isolated test environment and contains no exploit code, malware, or offensive tooling.

<br>

## Key Highlights

- **Behavior-based ransomware detection** using multi-signal risk scoring
- **80+ risk score** threshold for confirmed ransomware incidents
- **70+ antivirus engines** through VirusTotal hash reputation
- **5 MITRE ATT&CK techniques** mapped across detected threats
- Real-time monitoring of files and processes
- Automated **containment, quarantine, and file recovery**
- **Canary files, YARA, entropy analysis, and hash reputation** for layered detection
- IOC search and threat-hunting capabilities
- Real-time SOC dashboard with WebSocket alerts
- PDF incident reporting

<br>

## Problem Statement

Traditional signature-based security tools may fail to identify previously unseen ransomware behavior. Ransomware can begin encrypting or modifying files before a known signature becomes available.

RansomGuard addresses this challenge by monitoring **behavioral indicators** such as:

- Rapid file modifications and renaming
- High-entropy file writes
- Access to protected canary files
- Suspicious process activity
- YARA rule matches
- Malicious or suspicious file-hash reputation
- Anti-recovery behavior

These signals are combined into a weighted risk score to support faster threat identification and response.

<br>

## Core Features

### Behavioral Threat Detection

RansomGuard continuously monitors endpoint activity instead of relying only on known malware signatures.

- Real-time file creation, modification, rename, and deletion monitoring
- Running-process monitoring
- Shannon entropy analysis for encrypted-looking content
- Canary-file monitoring
- YARA-based pattern detection
- SHA-256 hash reputation through VirusTotal

### Risk Assessment

Multiple security signals are combined into a weighted detection score.

| Signal | Purpose |
|---|---|
| File Entropy | Identifies encrypted-looking content |
| Canary Files | Detects suspicious access to protected decoy files |
| File Behavior | Identifies rapid modification and rename activity |
| Process Behavior | Detects suspicious process activity |
| YARA | Detects ransomware-related patterns |
| VirusTotal | Provides hash-based reputation information |

A score of **80 or higher** confirms ransomware according to the configured detection engine.

### Sensitive File Protection

RansomGuard focuses on protecting monitored files from ransomware-driven modification and loss.

- Monitors configured folders in real time
- Detects suspicious file modifications
- Uses canary documents as high-confidence indicators
- Maintains scheduled backups of watched folders
- Restores affected files after confirmed detection

### Incident Response

The platform supports an end-to-end detection and response workflow.

```text
Detect
  ↓
Risk Score
  ↓
Confirm Incident
  ↓
MITRE ATT&CK Mapping
  ↓
Contain Process
  ↓
Quarantine Executable
  ↓
Restore Affected Files
  ↓
Generate Incident Reportardening.</sub>
</div>
