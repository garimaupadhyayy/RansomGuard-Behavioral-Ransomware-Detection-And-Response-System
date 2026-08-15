<div align="center">

# RansomGuard

**Behavioral Ransomware Detection, Containment & Automated Recovery Platform**

![alt text](<Screenshot 2026-08-15 231058.png>)

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.4-4479A1?logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

</div>

<br>

## Overview

RansomGuard is a self-hosted, local-first EDR (Endpoint Detection & Response) system that detects ransomware through **behavioral analysis** rather than signature matching. It watches file-system and process activity in real time, scores that behavior against a weighted detection engine, maps confirmed threats to MITRE ATT&CK techniques, and — depending on the configured mode — automatically contains the responsible process, quarantines its executable, and restores affected files from backup. Every stage of that pipeline is visible live on a dedicated SOC-style dashboard.

This is an educational, defensive-security project. It contains no exploit code, malware, or offensive tooling of any kind — only detection and response logic, exercised against simulated ransomware *behavior* (rapid renaming, high-entropy writes) inside an isolated test environment.

> **Runs entirely on your own machine.** There is no hosted or cloud version — RansomGuard is a local security tool you run and operate yourself, described below.

<br>

## Why This Project

Most portfolio security projects are static — a scanner you run once, a checklist. RansomGuard is a continuously running system that demonstrates:

- **Behavioral detection engineering** — weighted, multi-signal scoring instead of brittle signature matching
- **End-to-end incident response** — detect, contain, and recover automatically, not just alert
- **Threat intelligence integration** — VirusTotal hash reputation and YARA pattern rules
- **MITRE ATT&CK mapping** — every alert tagged to a real technique ID
- **Operational SOC tooling** — a live, WebSocket-driven dashboard built the way an analyst would actually use one

<br>

## Features

| Category | Capability |
|---|---|
| File monitoring | Real-time create/modify/rename/delete tracking via `watchdog` |
| Process monitoring | Tracks running processes — PID, parent, hash, CPU/memory — via `psutil` |
| Entropy detection | Flags encrypted-looking content (Shannon entropy ≥ 7.5) |
| Canary files | Deploys decoy documents (`passwords.docx`, `salary.xlsx`); any access is treated as a high-confidence signal |
| Weighted risk engine | Combines every signal into a single score; confirmed ransomware at score ≥ 80 |
| MITRE ATT&CK mapping | Every alert tagged with matching technique IDs (T1486, T1490, T1083, T1057, T1105) |
| VirusTotal integration | SHA-256 hash lookups against 70+ antivirus engines |
| YARA rule scanning | Pattern-based detection for ransom-note text and anti-recovery commands |
| Scheduled backup & recovery | Periodic snapshots of watched folders; automatic restore on confirmed detection |
| Process containment & quarantine | Kills malicious processes and isolates their executables |
| IOC search / threat hunting | Search recorded hashes, filenames, and paths across the full event history |
| PDF incident reports | One-click, analyst-style report generation per incident |
| Live dashboard | Alerts, timeline, MITRE matrix, and quarantine state — all updated over WebSocket |
| Simulation Mode | A safety switch: detect and alert without ever killing, quarantining, or restoring anything for real |

<br>

## Architecture

```
                    ┌───────────────────────────┐
                    │   React + TypeScript UI     │
                    │   SOC Dashboard (Vite)      │
                    └──────────────┬───────────────┘
                                   │ REST + WebSocket
                    ┌──────────────▼───────────────┐
                    │        FastAPI Backend        │
                    │  Detection Engine · MITRE      │
                    │  Alerts · Backup · Restore     │
                    │  Quarantine · Reports          │
                    └──────┬─────────────────┬──────┘
                           │                 │
              ┌────────────▼───────┐ ┌───────▼────────────┐
              │   File Watcher       │ │   Process Watcher    │
              │   (watchdog)          │ │   (psutil)            │
              │   entropy · YARA ·    │ │   hash reputation ·   │
              │   canary files        │ │   containment         │
              └───────────────────────┘ └───────────────────────┘
                           │
                    ┌──────▼──────┐
                    │ MySQL + Redis │
                    │ persistence /  │
                    │ caching layer  │
                    └───────────────┘
```

**Detection pipeline:** file/process event → signal extraction (entropy, extension, canary hit, hash reputation, YARA match) → weighted score → MITRE technique mapping → alert (and incident, if score ≥ 80) → response (restore/contain, or simulated) → broadcast to the dashboard in real time.

<br>

## Tech Stack

| Layer | Technologies |
|---|---|
| Backend | Python, FastAPI, SQLAlchemy, MySQL, Redis, JWT auth, WebSockets, `watchdog`, `psutil`, `yara-python`, `reportlab` |
| Frontend | React 18, TypeScript, Vite, Recharts, `lucide-react` |
| Infrastructure | Docker Compose (MySQL + Redis) |

<br>

## How It Runs

RansomGuard has three moving parts that all run on your own machine, side by side, every time you use it:

1. **Docker containers** — MySQL and Redis, providing persistence and caching
2. **Backend** — a FastAPI process that runs the file watcher, process watcher, and detection engine
3. **Frontend** — a Vite dev server serving the React dashboard in your browser

All three need to be running at the same time for the system to work. Closing any of them stops that part of the pipeline; starting them again resumes monitoring from where the database left off.

<br>

## Setup

### Prerequisites
- Docker Desktop
- Python 3.11+
- Node.js 18+

### 1. Clone the repository
```bash
git clone https://github.com/garimaupadhyayy/RansomGuard-Behavioral-Ransomware-Detection-And-Response-System.git
cd RansomGuard-Behavioral-Ransomware-Detection-And-Response-System
```

### 2. Configure environment variables
```bash
cp .env.example backend/.env
```
Then edit `backend/.env`:
- Add a free [VirusTotal API key](https://www.virustotal.com/gui/join-us) to enable hash reputation lookups (optional — lookups are simply skipped without one)
- Set `WATCH_FOLDERS` to the folder(s) you want monitored
- Leave `SIMULATION_MODE=true` until you've validated the detection engine — this prevents any real process kill, quarantine, or file restore from happening

### 3. Start the database layer
```bash
docker compose up -d
```
This brings up MySQL and Redis in the background.

### 4. Start the backend
```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
This starts the API server and both background watchers, and exposes interactive API documentation.

### 5. Start the frontend
In a separate terminal:
```bash
cd frontend
npm install
npm run dev
```
This starts the dashboard.

### 6. Trigger a safe test detection
This simulates ransomware *behavior* only — no real malicious code — to confirm the pipeline works end to end:
```bash
cd backend/test_folder
for i in $(seq 1 20); do echo "test data $i" > file$i.txt; mv file$i.txt file$i.locked; done
```
An alert should appear on the dashboard's Live Alerts view within seconds.

<br>

## API Reference

| Endpoint | Description |
|---|---|
| `GET /api/events/files` | Recent file events |
| `GET /api/events/processes` | Recent process events |
| `GET /api/alerts` | All triggered alerts |
| `GET /api/incidents` | Confirmed incidents |
| `GET /api/incidents/{id}/report` | Generate a PDF incident report |
| `GET /api/quarantine` | Isolated files and processes |
| `GET /api/ioc/search?q=` | Search hashes, filenames, and paths |
| `GET /api/hunt/unsigned-processes` | Threat hunting: unknown processes |
| `GET /api/hunt/script-hosts` | Threat hunting: PowerShell/CMD/WScript activity |
| `GET /api/virustotal/lookup/{sha256}` | Manual VirusTotal hash check |
| `GET /api/mitre/summary` | Alert counts per MITRE technique |
| `POST /api/auth/register`, `/login` | Account creation and JWT token issuance |
| `WS /api/ws/alerts` | Live alert stream |

<br>

## Safety Design

- **`SIMULATION_MODE=true` by default** — the system detects and alerts, but never kills a process, quarantines a file, or restores anything for real, until this is explicitly disabled.
- Internal project directories (`backups`, `.git`, `node_modules`, `venv`, `quarantine_storage`) are automatically excluded from monitoring to prevent feedback loops.
- Built strictly for educational and defensive security purposes. Contains no code capable of causing harm.

<br>

## Roadmap

- Lock all API routes behind JWT authentication
- Windows-specific containment: Firewall isolation, Volume Shadow Copy checks
- Expand the YARA rule set with community ransomware signatures
- Role-based access control for multi-analyst use

<br>

## License

Released under the [MIT License](LICENSE).

<br>

<div align="center">
<sub>A defensive security learning project. Not intended for production deployment without further hardening.</sub>
</div>