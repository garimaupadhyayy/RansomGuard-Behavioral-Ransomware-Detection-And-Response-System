<div align="center">
🛡️ RansomGuard
Real-Time Ransomware Detection & Auto-Recovery System

A behavioral EDR (Endpoint Detection & Response) platform that detects ransomware activity through file-system and process behavior — not signatures — and automatically contains, recovers, and reports on incidents through a live SOC dashboard.

Show Image Show Image Show Image Show Image Show Image Show Image Show Image Show Image

</div>
Overview

RansomGuard continuously monitors file-system and process activity, scores behavior using a weighted detection engine (rapid renames, high file entropy, canary-file access, unsigned binaries, VirusTotal hash reputation), maps confirmed threats to MITRE ATT&CK techniques, and — depending on mode — automatically contains the process, quarantines the executable, and restores affected files from backup. Every detection, incident, and response action is visible live on a React/TypeScript SOC dashboard.

Built as an educational, defensive-security project. It contains no real malware, exploit code, or offensive tooling — only detection and response logic, exercised safely against simulated ransomware behavior (rapid renaming, high-entropy writes) in an isolated test environment.

Why this project

Most portfolio security projects are static (a scanner, a checklist). RansomGuard is a live system that demonstrates:

Behavioral detection engineering — weighted scoring instead of brittle signature matching
Incident response automation — detect → contain → recover, end to end
Threat intelligence integration — VirusTotal hash reputation, YARA pattern rules
MITRE ATT&CK mapping — alerts tagged to real technique IDs (T1486, T1490, T1083, T1057, T1105)
SOC tooling UX — a live, WebSocket-driven dashboard a real analyst could use
Features
Category	What it does
🔍 File monitoring	Watches folders in real time (create/modify/rename/delete) via watchdog
⚙️ Process monitoring	Tracks running processes (PID, parent, hash, CPU/memory) via psutil
🎲 Entropy detection	Flags encrypted-looking file content (Shannon entropy ≥ 7.5)
🐤 Canary files	Deploys decoy documents (passwords.docx, salary.xlsx) — any access is an instant high-confidence signal
🧮 Weighted risk engine	Combines signals into a single score; confirmed ransomware at score ≥ 80
🗺️ MITRE ATT&CK mapping	Every alert tagged with matching technique IDs
🦠 VirusTotal integration	SHA-256 hash lookups against 70+ AV engines
🧬 YARA rule scanning	Pattern-based detection for ransom notes and anti-recovery commands
💾 Scheduled backup & auto-recovery	Periodic snapshots; automatic restore on confirmed detection
🔒 Process containment & quarantine	Kills malicious processes, isolates their executables
🕵️ IOC search / threat hunting	Search hashes, filenames, and paths across all recorded events
📄 PDF incident reports	One-click, analyst-style report generation per incident
📡 Live WebSocket dashboard	Alerts, timeline, MITRE matrix, and quarantine — all real time
🧪 Simulation Mode	Safety switch — detect and alert without ever killing/quarantining/restoring for real
Architecture
┌─────────────────────┐      ┌──────────────────────┐      ┌─────────────────────┐
│  React + TypeScript │◄────►│   FastAPI Backend     │◄────►│   MySQL + Redis     │
│  SOC Dashboard       │ WS/  │   Detection Engine    │      │   Persistence /     │
│  (Vite, Recharts)    │ REST │   Alert / MITRE /      │      │   caching layer     │
└─────────────────────┘      │   Backup / Restore /   │      └─────────────────────┘
                              │   Quarantine / Reports │
                              └──────────┬────────────┘
                                         │
                       ┌─────────────────┴─────────────────┐
                       │                                     │
              ┌────────▼────────┐                  ┌────────▼────────┐
              │  File Watcher     │                  │  Process Watcher │
              │  (watchdog)       │                  │  (psutil)        │
              │  entropy · YARA · │                  │  hash · VirusTotal│
              │  canary files     │                  │  containment      │
              └───────────────────┘                  └───────────────────┘

Detection flow: file/process event → signal extraction (entropy, extension, canary, hash reputation, YARA) → weighted score → MITRE mapping → alert (+ incident, if score ≥ 80) → response (restore / contain — or simulated, if Simulation Mode is on) → broadcast to dashboard via WebSocket.

Tech Stack

Backend: Python, FastAPI, SQLAlchemy, MySQL, Redis, JWT auth, WebSockets, watchdog, psutil, yara-python, reportlab Frontend: React 18, TypeScript, Vite, Recharts, lucide-react Infra: Docker Compose (MySQL + Redis)

Screenshots

Add dashboard screenshots here once deployed — Overview (charts), Live Alerts, Incident Timeline, MITRE Matrix.

Getting Started
Prerequisites
Docker Desktop
Python 3.11+
Node.js 18+
1. Clone & configure
bash
git clone https://github.com/garimaupadhyayy/RansomGuard-Behavioral-Ransomware-Detection-And-Response-System
cd ransomguard
cp .env.example backend/.env

Edit backend/.env:

Add a free VirusTotal API key (optional — hash lookups are skipped without it)
Set WATCH_FOLDERS to the folder(s) you want monitored
Leave SIMULATION_MODE=true until you trust the detection engine on real data
2. Start the databases
bash
docker compose up -d
3. Start the backend
bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

API docs: http://localhost:8000/docs

4. Start the frontend
bash
cd frontend
npm install
npm run dev

Dashboard: http://localhost:5173

5. Trigger a safe test detection
bash
cd backend/test_folder
for i in $(seq 1 20); do echo "test data $i" > file$i.txt; mv file$i.txt file$i.locked; done

Watch the alert appear live on the Live Alerts tab.

API Reference
Endpoint	Description
GET /api/events/files	Recent file events
GET /api/events/processes	Recent process events
GET /api/alerts	All triggered alerts
GET /api/incidents	Confirmed incidents
GET /api/incidents/{id}/report	Generate a PDF report
GET /api/quarantine	Isolated files/processes
GET /api/ioc/search?q=	Search hashes/filenames/paths
GET /api/hunt/unsigned-processes	Threat hunting: unknown processes
GET /api/hunt/script-hosts	Threat hunting: PowerShell/CMD/WScript activity
GET /api/virustotal/lookup/{sha256}	Manual VirusTotal hash check
GET /api/mitre/summary	Alert counts per MITRE technique
POST /api/auth/register / /login	Account + JWT token
WS /api/ws/alerts	Live alert stream
Safety Notes
SIMULATION_MODE=true (default) — detects and alerts, but never kills a process, quarantines a file, or restores anything for real. Recommended until the detection engine has been validated.
Internal project folders (backups, .git, node_modules, venv, quarantine_storage) are automatically excluded from monitoring to prevent feedback loops.
This project is for educational and defensive security purposes only. It does not contain, generate, or distribute malicious code.
Roadmap
 Lock API routes behind JWT auth
 Windows-specific containment (Firewall isolation, Volume Shadow Copy checks)
 Expand YARA rule set with community ransomware signatures
 Role-based access control for multi-analyst SOC use
License

MIT — see LICENSE for details.

<div align="center"> <sub>Built as a defensive security learning project. Not intended for production use without further hardening.</sub> </div>