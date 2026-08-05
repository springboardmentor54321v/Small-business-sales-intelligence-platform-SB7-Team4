# DevOps & System Integration Layer — Milestone 3 Completion

This document lists the checkpoints completed for the **Database & DevOps Engineer (Intern 5)** role as specified in the Milestone 3 Software Requirements Specification, including how each checkpoint was approached and implemented.

---

### Daily Checkpoints & Work Done

#### Day 1: Plan Infrastructure & Milestone Scope
* **Approach & Work Done**: Reviewed project setup and mapped out integration requirements. Authored an infrastructure plan detailing the addition of the new notifications microservice, CI pipelines, and health monitoring tools. Highlighted to the team that live hosting is deferred to Milestone 4.

#### Day 2: Notifications Service Containerization
* **Approach & Work Done**: Created a dedicated Dockerfile blueprint for the new Notifications service (`notifications.Dockerfile`). Updated the shared `docker-compose.yml` file to orchestrate the new container alongside existing services (linked over ports and networks).

#### Day 3: CI Pipeline Setup for Backend & Frontend Tests
* **Approach & Work Done**: Configured the GitHub Actions workflow (`ci.yml`) to automatically run the Python backend tests (`test_backend_ci.py` and the core `Backend_Database/tests/` unit/integration test cases) and the frontend Streamlit check suite on every push.

#### Day 4: CI Pipeline Setup for Security Tests
* **Approach & Work Done**: Expanded the CI workflow to execute the API Gateway integration test suite (`test_gateway.py`) and the 55-check security matrix audit script (`test_security_audit.py`) on every push to verify security constraints automatically.

#### Day 5: Set up Local Monitoring Helper
* **Approach & Work Done**: Developed an automated health check monitor script (`health_check.py`) that executes requests to all microservices (Gateway, Backend, ML, Frontend, Notifications) and outputs their online statuses and round-trip response latencies.

#### Day 6: Rehearse Backup and Restore Process
* **Approach & Work Done**: Rehearsed data retention procedures by running the backup and restore utility script (`backup_restore.py`). Verified that system tables are successfully dumped to JSON files and can be restored back without issues.

#### Day 7: Prepare Milestone 4 Deployment Configuration
* **Approach & Work Done**: Prepared the Render configuration blueprint (`render.yaml`) and compiled a step-by-step deployment guide outlining variables and environment setups for the upcoming hosting phase.

#### Day 8: Coordinate Local Integration
* **Approach & Work Done**: Resolved environment variable requirements and port maps between services. Configured SQLite fallback database paths and thread configurations to prevent backend runtime errors during testing.

#### Day 9: Run Full End-to-End System Tests
* **Approach & Work Done**: Ran automated verification test suites across all backend, DevOps, and security files, confirming that the entire application flows pass successfully.

#### Day 10: Finalize Local Integration and Demos
* **Approach & Work Done**: Re-tested and confirmed that the entire multi-container environment starts and links together cleanly with a single, simple command (`docker compose up -d`). Finalized deployment preparation notes.
