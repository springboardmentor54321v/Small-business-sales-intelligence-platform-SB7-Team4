# DevOps Infrastructure & Orchestration Plan (Milestone 3)

This plan details the infrastructure, container orchestration, and continuous integration upgrades for Milestone 3.

---

## 1. Container Orchestration Upgrade

We are introducing a new container service for **Notifications** to support alert dispatch:
* **Container Name**: `notifications`
* **Internal Port**: `5003`
* **Technology**: Python (FastAPI/Flask) lightweight service.
* **Volume Persistence**: Reuses existing shared network links.

```yaml
notifications:
  build:
    context: .
    dockerfile: DevOps_Integration/notifications/Dockerfile
  ports:
    - "5003:5003"
  environment:
    - PORT=5003
```

---

## 2. CI/CD Validation Strategy (GitHub Actions)

We will configure GitHub Actions to automatically run verification steps on every push:
1. **Python Compilation Validation**: Compile all Python scripts to check syntax.
2. **Security Gateway Test Suite**: Run `test_gateway.py` integration tests verifying all 25+ RBAC checks.
3. **Backend Database Tests**: Run backend tests to verify database integrity.
4. **Dockerfile Validation**: Build checking syntax structure of all 5 Dockerfiles (`gateway`, `backend`, `frontend`, `aiml`, `notifications`).

---

## 3. Local Uptime Monitoring & Rehearsal

* **Monitoring**: We will expand `health_check.py` to ping the new Notifications container on Port 5003, tracking latency.
* **Backups**: Rehearse database export/restore procedures using `backup_restore.py` on the unchanged Milestone 2 dataset.

---

## ⚠️ Golden Rule Reminder: No Live Cloud Deployment

* As per Section 1.4 of the Milestone 3 specification, **deployment to a live public web link is intentionally saved for Milestone 4**.
* All Milestone 3 features will run locally inside the `docker-compose` environment. DevOps will prepare configuration blueprints but will not execute any live deployment pipelines during this milestone.
