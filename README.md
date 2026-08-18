# MarketMind AI — Small Business Sales Intelligence Platform
> **AI-powered sales intelligence platform designed to help small businesses, retail stores, supermarkets, and startups make data-driven business decisions using machine learning and real-time analytics.**

---

## 🏗️ Architecture Overview

The platform consists of 4 integrated microservices:

| Service | Technology | Port | Description |
| :--- | :--- | :---: | :--- |
| **Frontend Dashboard** | Streamlit + Plotly | `8501` | Interactive analytics UI, forecasts, customer & inventory management |
| **Security API Gateway** | FastAPI + JWT | `5000` | Rate limiting, authentication, request routing, audit logs |
| **Database Backend API** | FastAPI + SQLAlchemy | `8000` | Core CRUD operations, transaction management, SQLite/PostgreSQL |
| **AI/ML Engine** | Flask + CatBoost + Scikit-learn | `5002` | Sales forecasting, churn prediction, segmentation, anomaly detection |

---

## 🚀 Quick Start Guide (Run Locally)

### Prerequisites
- **Python 3.10+** installed ([python.org](https://www.python.org/downloads/))
- **Git** installed ([git-scm.com](https://git-scm.com/))

---

### Step 1: Clone the Repository
```bash
git clone https://github.com/springboardmentor54321v/Small-business-sales-intelligence-platform-SB7-Team4.git
cd Small-business-sales-intelligence-platform-SB7-Team4
```

---

### Step 2: Install Python Dependencies

#### Option A: One-Command Installation (All Services)
```bash
pip install -r Backend_Database/requirements.txt
pip install -r Security_APIGateway/requirements.txt
pip install -r AIML/requirements.txt
pip install -r frontend/requirements.txt
```

*(Optional: You can create and activate a virtual environment first: `python -m venv venv`, then `venv\Scripts\activate` on Windows or `source venv/bin/activate` on Mac/Linux).*

---

### Step 3: Run the Services

#### ⚡ Option A: Windows 1-Click Launch (Recommended for Windows)
Simply double-click **`start_local.bat`** or run in PowerShell:
```powershell
.\start_local.ps1
```
> *This automatically opens 4 terminal windows and starts all microservices with the proper environment variables.*

To stop all running services later, run:
```powershell
.\stop_local.ps1
```
*(or double-click `stop_local.bat`)*.

---

#### 💻 Option B: Manual Terminal Launch (Cross-Platform: Windows / macOS / Linux)

Open 4 separate terminal windows in the repository root folder:

#### Terminal 1 — Database Backend API (Port 8000)
```bash
# Windows (PowerShell)
cd Backend_Database
$env:DATABASE_URL="sqlite:///./marketmind.db"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# macOS / Linux (Bash)
cd Backend_Database
export DATABASE_URL="sqlite:///./marketmind.db"
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Terminal 2 — AI/ML Analytics Engine (Port 5002)
```bash
# Windows (PowerShell)
$env:PORT="5002"
python AIML/Integrated_API/app.py

# macOS / Linux (Bash)
export PORT=5002
python3 AIML/Integrated_API/app.py
```

#### Terminal 3 — Security API Gateway (Port 5000)
```bash
# Windows (PowerShell)
$env:BACKEND_URL="http://localhost:8000"
$env:AI_URL="http://localhost:5002"
$env:JWT_SECRET="local_secret_key_12345"
python -m uvicorn Security_APIGateway.server:app --host 0.0.0.0 --port 5000 --reload

# macOS / Linux (Bash)
export BACKEND_URL="http://localhost:8000"
export AI_URL="http://localhost:5002"
export JWT_SECRET="local_secret_key_12345"
python3 -m uvicorn Security_APIGateway.server:app --host 0.0.0.0 --port 5000 --reload
```

#### Terminal 4 — Streamlit Frontend UI (Port 8501)
```bash
# Windows (PowerShell)
$env:AUTH_BASE_URL="http://localhost:5000"
$env:DB_BASE_URL="http://localhost:8000"
python -m streamlit run frontend/app.py

# macOS / Linux (Bash)
export AUTH_BASE_URL="http://localhost:5000"
export DB_BASE_URL="http://localhost:8000"
python3 -m streamlit run frontend/app.py
```

---

### 🐳 Option C: Run via Docker Compose (If Docker is installed)
```bash
docker compose -f DevOps_Integration/docker-compose.yml up --build
```

---

## 🌐 Local Application Endpoints

Once started, open your browser:

- **🖥️ Frontend Web App:** [http://localhost:8501](http://localhost:8501)
- **🛡️ API Security Gateway Docs:** [http://localhost:5000/docs](http://localhost:5000/docs)
- **🗄️ Backend Database Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **🤖 AI/ML Analytics API:** [http://localhost:5002](http://localhost:5002)

---

## 🩺 System Health Check
To verify that all 4 local microservices are online and communicating properly:
```bash
python DevOps_Integration/scripts/health_check.py
```
