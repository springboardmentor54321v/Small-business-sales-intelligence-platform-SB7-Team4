# MarketMind AI - Local Multi-Service Launcher (Windows PowerShell)
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "     MarketMind AI - Starting Local Services      " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$ROOT_DIR = $PSScriptRoot

# 1. Start Backend API (FastAPI) on Port 8000
Write-Host "[1/4] Launching Database Backend API (Port 8000)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$ROOT_DIR\Backend_Database'; `$env:DATABASE_URL='sqlite:///./marketmind.db'; python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

# 2. Start AI/ML Analytics Engine on Port 5002
Write-Host "[2/4] Launching AI/ML Analytics Service (Port 5002)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$ROOT_DIR'; `$env:PORT='5002'; python AIML/Integrated_API/app.py"

# 3. Start Security API Gateway on Port 5000
Write-Host "[3/4] Launching Security API Gateway (Port 5000)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$ROOT_DIR'; `$env:BACKEND_URL='http://localhost:8000'; `$env:AI_URL='http://localhost:5002'; `$env:JWT_SECRET='local_secret_key_12345'; python -m uvicorn Security_APIGateway.server:app --host 0.0.0.0 --port 5000 --reload"

# Wait 3 seconds for backend services to initialize
Start-Sleep -Seconds 3

# 4. Start Streamlit Frontend UI on Port 8501
Write-Host "[4/4] Launching Streamlit Frontend Dashboard..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$ROOT_DIR'; `$env:AUTH_BASE_URL='http://localhost:5000'; `$env:DB_BASE_URL='http://localhost:8000'; python -m streamlit run frontend/app.py"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "All services launched in separate windows!" -ForegroundColor Yellow
Write-Host "- Streamlit Frontend: http://localhost:8501" -ForegroundColor White
Write-Host "- Security API Gateway: http://localhost:5000/docs" -ForegroundColor White
Write-Host "- Backend Database API: http://localhost:8000/docs" -ForegroundColor White
Write-Host "- AI/ML Analytics API:  http://localhost:5002" -ForegroundColor White
Write-Host "==================================================" -ForegroundColor Cyan
