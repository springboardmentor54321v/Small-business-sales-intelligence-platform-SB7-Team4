import os
import datetime
from typing import List, Dict, Optional
import jwt
import bcrypt
from fastapi import FastAPI, Depends, HTTPException, Header, status
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
    
    # Generate JWT Token
    exp_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=24)
    payload = {
        "userId": user["id"],
        "name": user["name"],
        "role": user["role"],
        "exp": int(exp_time.timestamp()),
        "iat": int(datetime.datetime.now(datetime.UTC).timestamp())
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)
    
    log_audit(f"User Logged In: {user['name']} (Role: {user['role']})")
    
    return {
        "message": "Login successful",
        "token": token,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }

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

# --- Proxy Route Stubs ---

@app.post("/api/sales/upload")
async def proxy_sales_upload(user: Dict = Depends(check_role(["Business Owner", "Store Manager", "Sales Executive"]))):
    return {
        "message": "[Proxy: Gateway] Sales upload route stub hit successfully. Authorized.",
        "requestUser": user
    }

@app.get("/api/sales/dashboard-metrics")
async def proxy_sales_metrics(user: Dict = Depends(check_role(["Business Owner", "Store Manager"]))):
    return {
        "message": "[Proxy: Gateway] Dashboard metrics stub hit successfully. Authorized.",
        "requestUser": user
    }

@app.get("/api/inventory")
async def proxy_inventory_view(user: Dict = Depends(check_role(["Business Owner", "Store Manager", "Sales Executive"]))):
    return {
        "message": "[Proxy: Gateway] Inventory view stub hit successfully. Authorized.",
        "requestUser": user
    }

@app.post("/api/inventory/update")
async def proxy_inventory_update(user: Dict = Depends(check_role(["Business Owner", "Store Manager"]))):
    return {
        "message": "[Proxy: Gateway] Inventory edit stub hit successfully. Authorized.",
        "requestUser": user
    }

@app.get("/api/forecast/sample")
async def proxy_forecast_sample(user: Dict = Depends(check_role(["Business Owner"]))):
    return {
        "message": "[Proxy: Gateway] Forecasting stub hit successfully. Authorized.",
        "requestUser": user
    }

@app.get("/api/audit-logs")
async def proxy_audit_logs(user: Dict = Depends(check_role(["System Administrator"]))):
    return {
        "message": "[Proxy: Gateway] System audit logs stub hit successfully. Authorized.",
        "requestUser": user
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=5000, log_level="info")
