# DevOps & System Integration Layer

In this part of the project, I built the system integration, containerization scripts, local presentation dashboard, and CI workflows to unite all services into a single, deployable development environment for Milestone 1.

---

## 1. What I Built for Milestone 1

### Service Containerization & Context Routing
I created dedicated Dockerfile blueprints for every microservice to package them as lightweight, repeatable containers. To keep the repository clean and avoid modifying other team members' code directories, I placed all Dockerfiles inside the `DevOps_Integration/` folder:
- **`gateway.Dockerfile`**: Containerizes the FastAPI security layer on Port 5000.
- **`backend.Dockerfile`**: Containerizes the PostgreSQL backend app on Port 8000.
- **`aiml.Dockerfile`**: Containerizes the Flask forecasting stub service on Port 5000 (mapped to Port 5002 on host).
- **`frontend.Dockerfile`**: Containerizes Nginx to host our client dashboard on Port 3000.

### Dynamic Multi-Container Orchestration
I authored the root `docker-compose.yml` file to manage and spin up all five containers simultaneously. It defines an isolated network where services can communicate with each other using domain hostnames (e.g., `db`, `backend`, `aiml`, `gateway`). I configured a database health check that blocks the backend from running until PostgreSQL is ready, and wired up environment parameters (like `DATABASE_URL`, `BACKEND_URL`, and `AI_URL`) to link the components together seamlessly.

### Integrated Presentation Dashboard Client
Since the team's frontend folder was empty, I developed a single-page application inside `DevOps_Integration/frontend/` to serve as a visual demo interface for Milestone 1. Serviced via Nginx, this dashboard connects to the API Gateway on Port 5000 and supports user registration, login JWT storage, role-specific sidebar navigation, drag-and-drop CSV dataset ingestion, stock adjustment forms, and query engines that fetch forecasts.

### Continuous Integration Workflow
I created the automated GitHub Actions pipeline in `.github/workflows/ci.yml`. On every code push or pull request to the `main` branch, the workflow triggers:
1. Syntax compilation verification for all python scripts inside both the gateway and the database backend.
2. Pre-build validations of all four custom docker containers, guaranteeing that any code additions do not break container builds.

---

## 2. Port Mappings & Service Discovery

When running, the environment exposes the following ports on your local host:
* **Frontend Web Dashboard**: `http://localhost:3000` (Nginx static content server)
* **API Security Gateway**: `http://localhost:5000` (Proxies all backend traffic)
* **Backend Database API**: `http://localhost:8000` (Handles schemas and PostgreSQL operations)
* **AI Forecasting API**: `http://localhost:5002` (Flask machine learning forecasting stub)
* **PostgreSQL Database**: `localhost:5432` (Relational persistent storage)

---

## 3. How to Run the Environment

### Prerequisites
Make sure you have Docker and Docker Compose installed and running on your system.

### Build and Launch the Stack
Run the following commands in the root directory of your workspace to compile the containers and start the network:
```powershell
# Build all custom service containers
docker-compose build

# Start the environment in the background
docker-compose up -d
```

### Shutting Down the Stack
To stop all containers and tear down the virtual network, run:
```powershell
docker-compose down
```
