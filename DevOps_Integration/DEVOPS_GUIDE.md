# MarketMind AI — DevOps & Integration Guide (Milestone 2)

## 1. System Architecture Overview
The MarketMind AI platform is containerized as a microservices architecture orchestrated via Docker Compose:

| Container Name | Service | Internal Port | External Mapped Port |
| :--- | :--- | :---: | :---: |
| `marketmind_gateway` | API Security Gateway | 5000 | 5000 |
| `marketmind_backend` | Database Backend API | 8000 | 8000 |
| `marketmind_aiml` | AI/ML Analytics Engine | 5000 | 5002 |
| `marketmind_frontend` | Streamlit Dashboard UI | 8501 | 3000 / 8501 |
| `marketmind_db` | PostgreSQL Database | 5432 | 5432 |

---

## 2. Quick Start: Single-Command Launch

Launch the entire 5-container stack locally:
```powershell
docker compose -f DevOps_Integration/docker-compose.yml up -d --build
```
To verify running containers:
```powershell
docker compose -f DevOps_Integration/docker-compose.yml ps
```
To stop the platform:
```powershell
docker compose -f DevOps_Integration/docker-compose.yml down
```

---

## 3. Database Backup & Restore Procedure

### A. Creating an Automated Backup
Run the backup script to generate a timestamped dump:
```powershell
python DevOps_Integration/scripts/backup_restore.py backup
```
*Outputs timestamped JSON backups into `DevOps_Integration/backups/`.*

### B. Restoring from a Backup
To restore a specific backup dump:
```powershell
python DevOps_Integration/scripts/backup_restore.py restore DevOps_Integration/backups/<backup_filename>.json
```

---

## 4. Monitoring & Health Checks

Run the system health monitor to test latency and availability across all microservices:
```powershell
python DevOps_Integration/scripts/health_check.py
```

---

## 5. Automated CI/CD Pipeline
The GitHub Actions CI pipeline ([.github/workflows/ci.yml](file:///c:/Users/Punith%20Venkat%20Sai/OneDrive/Desktop/Infosys%20Springboard/DevOps_Integration/workflows/ci.yml)) automatically triggers on every pull request and push to `main` to:
1. Validate Python syntax across all services.
2. Build and verify all four Dockerfiles (`gateway.Dockerfile`, `backend.Dockerfile`, `aiml.Dockerfile`, `frontend.Dockerfile`).
