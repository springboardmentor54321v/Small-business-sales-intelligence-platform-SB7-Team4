import os
import datetime
from typing import List, Dict, Optional
import jwt
import bcrypt
import httpx
from fastapi import FastAPI, Depends, HTTPException, Header, status, File, UploadFile, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

app = FastAPI(
    title="MarketMind AI - API Gateway",
    description="API Gateway & Security Proxy Service for Small Business Sales Intelligence Platform",
    version="1.0.0"
)

# CORS configurations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

JWT_SECRET = os.getenv("JWT_SECRET", "marketmind-secret-key-12345")
ALGORITHM = "HS256"

# In-memory mock database for authentication testing
mock_users: List[Dict] = []
VALID_ROLES = [
    "Business Owner",
    "Store Manager",
    "Sales Executive",
    "System Administrator"
]

# Pydantic Schemas for validation
class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str

class LoginRequest(BaseModel):
    email: str
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

class InventoryUpdateSchema(BaseModel):
    product_id: int
    stock_quantity: int
    low_stock_threshold: int = 10

# Helper functions
def find_user_by_email(email: str) -> Optional[Dict]:
    for u in mock_users:
        if u["email"] == email:
            return u
    return None

def find_user_by_name(name: str) -> Optional[Dict]:
    for u in mock_users:
        if u["name"] == name:
            return u
    return None

# --- Custom Audit Logging ---
def log_audit(message: str, is_alert: bool = False):
    timestamp = datetime.datetime.now(datetime.UTC).isoformat()
    prefix = "[Audit Log - Alert]" if is_alert else "[Audit Log]"
    print(f"{prefix} - {timestamp} - {message}", flush=True)

# --- Authorization Dependencies ---

async def verify_token(authorization: Optional[str] = Header(None)) -> Dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token missing or malformed. Use Bearer <token>"
        )
    
    token = authorization.split(" ")[1]
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return decoded
    except jwt.ExpiredSignatureError:
        log_audit("Rejected expired token", is_alert=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is expired"
        )
    except jwt.InvalidTokenError as e:
        log_audit(f"Rejected invalid token: {str(e)}", is_alert=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is invalid"
        )

def check_role(allowed_roles: List[str]):
    async def role_dependency(user: Dict = Depends(verify_token)):
        if "role" not in user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: role signature missing"
            )
        if user["role"] not in allowed_roles:
            log_audit(
                f"Unauthorized role access attempt: User {user.get('name', 'unknown')} ({user['role']}) tried to access path",
                is_alert=True
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Forbidden: Access restricted. Required role: one of [{', '.join(allowed_roles)}]"
            )
        return user
    return role_dependency

# --- Authentication Routes ---

@app.post("/auth/register", status_code=status.HTTP_201_CREATED)
async def register(req: RegisterRequest):
    if req.role not in VALID_ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role. Must be one of: {', '.join(VALID_ROLES)}"
        )
    
    if find_user_by_email(req.email) or find_user_by_name(req.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or name already exists"
        )
    
    # Hash password
    salt = bcrypt.gensalt(10)
    password_bytes = req.password.encode('utf-8')
    password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

    new_user = {
        "id": len(mock_users) + 1,
        "name": req.name,
        "email": req.email,
        "password_hash": password_hash,
        "role": req.role,
        "refresh_tokens": [],  # Active refresh tokens list
        "created_at": datetime.datetime.now(datetime.UTC).isoformat()
    }
    mock_users.append(new_user)
    log_audit(f"User Registered: {req.name} as {req.role}")

    return {
        "message": "Registration successful",
        "user": {
            "id": new_user["id"],
            "name": new_user["name"],
            "email": new_user["email"],
            "role": new_user["role"],
            "created_at": new_user["created_at"]
        }
    }

@app.post("/auth/login")
async def login(req: LoginRequest):
    user = find_user_by_email(req.email)
    if not user:
        log_audit(f"Failed login attempt for non-existent email: {req.email}", is_alert=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Verify password hash
    password_bytes = req.password.encode('utf-8')
    user_hash_bytes = user["password_hash"].encode('utf-8')
    if not bcrypt.checkpw(password_bytes, user_hash_bytes):
        log_audit(f"Failed login attempt for user: {user['name']}", is_alert=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Generate short-lived Access Token (15 minutes)
    access_exp_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15)
    access_payload = {
        "userId": user["id"],
        "name": user["name"],
        "role": user["role"],
        "exp": int(access_exp_time.timestamp()),
        "iat": int(datetime.datetime.now(datetime.UTC).timestamp())
    }
    access_token = jwt.encode(access_payload, JWT_SECRET, algorithm=ALGORITHM)
    
    # Generate long-lived Refresh Token (7 days)
    refresh_exp_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=7)
    refresh_payload = {
        "userId": user["id"],
        "exp": int(refresh_exp_time.timestamp()),
        "iat": int(datetime.datetime.now(datetime.UTC).timestamp())
    }
    refresh_token = jwt.encode(refresh_payload, JWT_SECRET, algorithm=ALGORITHM)
    
    # Store refresh token in user's record
    if "refresh_tokens" not in user:
        user["refresh_tokens"] = []
    user["refresh_tokens"].append(refresh_token)
    
    log_audit(f"User Logged In: {user['name']} (Role: {user['role']})")
    
    return {
        "message": "Login successful",
        "token": access_token,
        "refreshToken": refresh_token,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }

@app.post("/auth/refresh")
async def refresh_token_route(req: RefreshRequest):
    try:
        decoded = jwt.decode(req.refresh_token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id = decoded.get("userId")
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is invalid"
        )

    # Verify user exists and token has not been revoked
    user = next((u for u in mock_users if u["id"] == user_id), None)
    if not user or "refresh_tokens" not in user or req.refresh_token not in user["refresh_tokens"]:
        log_audit(f"Rejected invalid or revoked refresh token for user ID: {user_id}", is_alert=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is revoked or invalid"
        )

    # Generate new Access Token (15 minutes)
    access_exp_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15)
    access_payload = {
        "userId": user["id"],
        "name": user["name"],
        "role": user["role"],
        "exp": int(access_exp_time.timestamp()),
        "iat": int(datetime.datetime.now(datetime.UTC).timestamp())
    }
    new_access_token = jwt.encode(access_payload, JWT_SECRET, algorithm=ALGORITHM)
    
    log_audit(f"Refreshed access token for user: {user['name']}")
    return {
        "token": new_access_token
    }

@app.post("/auth/logout")
async def logout(user: Dict = Depends(verify_token)):
    # Invalidate all active refresh tokens for the logged-out user
    user_record = next((u for u in mock_users if u["id"] == user.get("userId")), None)
    if user_record:
        user_record["refresh_tokens"] = []
        log_audit(f"User Logged Out: {user_record['name']} (revoked all refresh tokens)")
    
    return {"message": "Logged out successfully"}

# --- Authorization Dependencies ---

async def verify_token(authorization: Optional[str] = Header(None)) -> Dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token missing or malformed. Use Bearer <token>"
        )
    
    token = authorization.split(" ")[1]
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return decoded
    except jwt.ExpiredSignatureError:
        log_audit("Rejected expired token", is_alert=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is expired"
        )
    except jwt.InvalidTokenError as e:
        log_audit(f"Rejected invalid token: {str(e)}", is_alert=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is invalid"
        )

def check_role(allowed_roles: List[str]):
    async def role_dependency(user: Dict = Depends(verify_token)):
        if "role" not in user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: role signature missing"
            )
        if user["role"] not in allowed_roles:
            log_audit(
                f"Unauthorized role access attempt: User {user.get('name', 'unknown')} ({user['role']}) tried to access path",
                is_alert=True
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Forbidden: Access restricted. Required role: one of [{', '.join(allowed_roles)}]"
            )
        return user
    return role_dependency

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
AI_URL = os.getenv("AI_URL", "http://localhost:5002")

# --- Proxy Routes with Validation ---

@app.post("/api/sales/upload")
async def proxy_sales_upload(
    file: UploadFile = File(...),
    user: Dict = Depends(check_role(["Business Owner", "Store Manager", "Sales Executive"]))
):
    # Reject non-CSV uploads at the gateway layer
    if not file.filename.lower().endswith(".csv") and file.content_type != "text/csv":
        log_audit(f"Rejected non-CSV file upload attempt: {file.filename}", is_alert=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Malformed request: Only CSV files are allowed."
        )
    
    content = await file.read()
    
    async with httpx.AsyncClient() as client:
        try:
            files = {"file": (file.filename, content, file.content_type or "text/csv")}
            headers = {
                "x-user-id": str(user["userId"]),
                "x-user-role": user["role"]
            }
            # Proxy to the Backend_Database service
            response = await client.post(
                f"{BACKEND_URL}/api/sales/upload",
                files=files,
                headers=headers,
                timeout=30.0
            )
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except httpx.RequestError as e:
            log_audit(f"Connection failed to backend: {str(e)}", is_alert=True)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Database backend is unreachable: {str(e)}"
            )

@app.get("/api/sales/dashboard-metrics")
async def proxy_sales_metrics(
    request: Request,
    user: Dict = Depends(check_role(["Business Owner", "Store Manager"]))
):
    async with httpx.AsyncClient() as client:
        try:
            headers = {
                "x-user-id": str(user["userId"]),
                "x-user-role": user["role"]
            }
            response = await client.get(
                f"{BACKEND_URL}/api/sales/dashboard-metrics",
                params=dict(request.query_params),
                headers=headers
            )
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Database backend is unreachable"
            )

@app.get("/api/inventory")
async def proxy_inventory_view(
    request: Request,
    user: Dict = Depends(check_role(["Business Owner", "Store Manager", "Sales Executive"]))
):
    async with httpx.AsyncClient() as client:
        try:
            headers = {
                "x-user-id": str(user["userId"]),
                "x-user-role": user["role"]
            }
            response = await client.get(
                f"{BACKEND_URL}/api/inventory",
                params=dict(request.query_params),
                headers=headers
            )
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Database backend is unreachable"
            )

@app.post("/api/inventory/update")
async def proxy_inventory_update(
    payload: InventoryUpdateSchema,
    user: Dict = Depends(check_role(["Business Owner", "Store Manager"]))
):
    async with httpx.AsyncClient() as client:
        try:
            headers = {
                "x-user-id": str(user["userId"]),
                "x-user-role": user["role"]
            }
            response = await client.post(
                f"{BACKEND_URL}/api/inventory/update",
                json=payload.model_dump(),
                headers=headers
            )
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Database backend is unreachable"
            )

@app.get("/api/forecast/sample")
async def proxy_forecast_sample(
    request: Request,
    user: Dict = Depends(check_role(["Business Owner"]))
):
    async with httpx.AsyncClient() as client:
        try:
            headers = {
                "x-user-id": str(user["userId"]),
                "x-user-role": user["role"]
            }
            response = await client.get(
                f"{AI_URL}/api/forecast/sample",
                params=dict(request.query_params),
                headers=headers
            )
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except httpx.RequestError:
            # Fallback stub if AI service is not running
            return {
                "message": "[Gateway Fallback] AI/ML forecasting service is currently unreachable.",
                "requestUser": user
            }

@app.get("/api/audit-logs")
async def proxy_audit_logs(
    request: Request,
    user: Dict = Depends(check_role(["System Administrator"]))
):
    async with httpx.AsyncClient() as client:
        try:
            headers = {
                "x-user-id": str(user["userId"]),
                "x-user-role": user["role"]
            }
            response = await client.get(
                f"{BACKEND_URL}/api/audit-logs",
                params=dict(request.query_params),
                headers=headers
            )
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except httpx.RequestError:
            # Fallback stub for audit logs
            return {
                "message": "[Gateway Fallback] Audit logs backend is unreachable. Admin stubs active.",
                "requestUser": user
            }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=5000, log_level="info")
