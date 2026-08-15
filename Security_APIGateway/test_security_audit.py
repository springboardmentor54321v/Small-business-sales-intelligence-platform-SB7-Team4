# pyrefly: ignore-file
# type: ignore
import sys
import os
import time
import subprocess
import threading
import httpx
from fastapi import FastAPI, Header, status
from fastapi.responses import JSONResponse
import uvicorn

# Setup Mock Backend (reused from test_gateway.py)
mock_backend = FastAPI()

@mock_backend.get("/inventory/")
def mock_inventory(x_user_id: str = Header(None), x_user_role: str = Header(None)):
    return {"message": "Mock Inventory forward success", "injected_user_id": x_user_id, "injected_user_role": x_user_role}

@mock_backend.put("/inventory/{product_id}")
def mock_inventory_update(product_id: str, payload: dict, x_user_id: str = Header(None), x_user_role: str = Header(None)):
    return {"message": "Mock Inventory update forward success", "product_id": product_id, "payload": payload, "injected_user_id": x_user_id, "injected_user_role": x_user_role}

@mock_backend.post("/api/invoices")
def mock_create_invoice(payload: dict, x_user_id: str = Header(None), x_user_role: str = Header(None)):
    return {"message": "Mock Create Invoice forward success", "invoice_number": payload.get("invoice_number"), "total_amount": payload.get("total_amount"), "payment_status": payload.get("payment_status"), "injected_user_id": x_user_id, "injected_user_role": x_user_role}

@mock_backend.put("/api/invoices/{id}/status")
def mock_update_invoice_status(id: int, payload: dict, x_user_id: str = Header(None), x_user_role: str = Header(None)):
    return {"message": "Mock Update Invoice Status forward success", "invoice_id": id, "payment_status": payload.get("payment_status"), "injected_user_id": x_user_id, "injected_user_role": x_user_role}

@mock_backend.post("/invoices/bulk-update")
def mock_invoices_bulk_update(payload: dict, x_user_id: str = Header(None), x_user_role: str = Header(None)):
    return {"message": "Mock Invoices Bulk Update forward success", "injected_user_id": x_user_id, "injected_user_role": x_user_role}

@mock_backend.post("/inventory/bulk-update")
def mock_inventory_bulk_update(payload: dict, x_user_id: str = Header(None), x_user_role: str = Header(None)):
    return {"message": "Mock Inventory Bulk Update forward success", "injected_user_id": x_user_id, "injected_user_role": x_user_role}

@mock_backend.get("/api/invoices/revenue-summary")
def mock_revenue_summary(x_user_id: str = Header(None), x_user_role: str = Header(None)):
    return {"message": "Mock Revenue Summary forward success", "injected_user_id": x_user_id, "injected_user_role": x_user_role}

def run_mock_backend():
    uvicorn.run(mock_backend, host="127.0.0.1", port=8000, log_level="warning")

def run_security_audit():
    print("======================================================================")
    print("[SECURITY] RUNNING AUTOMATED SECURITY MATRIX AUDIT SCANNER (DAY 5)")
    print("======================================================================\n")

    # Start Mock Backend on 8000
    backend_thread = threading.Thread(target=run_mock_backend, daemon=True)
    backend_thread.start()
    time.sleep(1)

    # Spawn Gateway server on port 5000
    server_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "server:app", "--port", "5000"],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env={**os.environ, "TESTING": "true"}
    )

    # Wait for server to bind
    started = False
    for _ in range(30):
        time.sleep(0.5)
        if server_process.poll() is not None:
            print("Gateway server failed to start.")
            break
        try:
            with httpx.Client() as client:
                res = client.get("http://localhost:5000/docs")
                if res.status_code == 200:
                    started = True
                    break
        except Exception:
            continue

    if not started:
        print("Could not start API Gateway server.")
        if server_process.poll() is None:
            server_process.kill()
        sys.exit(1)

    base_url = "http://localhost:5000"
    
    # Register / Login Users to obtain tokens
    with httpx.Client() as client:
        # Register Owner
        reg_owner = client.post(f"{base_url}/auth/register", json={
            "name": "audit_owner", "email": "owner@audit.com", "password": "password123", "role": "Business Owner"
        }, headers={"x-bypass-rate-limit": "true"})
        print("Owner Register Status:", reg_owner.status_code, reg_owner.text)
        owner_tok_val = reg_owner.json().get("verification_token")
        ver_owner_res = client.post(f"{base_url}/auth/verify-email", json={"token": owner_tok_val}, headers={"x-bypass-rate-limit": "true"})
        print("Owner Verify Status:", ver_owner_res.status_code, ver_owner_res.text)
        
        owner_login = client.post(f"{base_url}/auth/login", json={"email": "owner@audit.com", "password": "password123"}, headers={"x-bypass-rate-limit": "true"}).json()
        owner_token = owner_login["token"]

        # Register Sales Executive
        reg_sales = client.post(f"{base_url}/auth/register", json={
            "name": "audit_sales", "email": "sales@audit.com", "password": "password123", "role": "Sales Executive"
        }, headers={"x-bypass-rate-limit": "true"})
        sales_tok_val = reg_sales.json().get("verification_token")
        client.post(f"{base_url}/auth/verify-email", json={"token": sales_tok_val}, headers={"x-bypass-rate-limit": "true"})
        
        sales_login = client.post(f"{base_url}/auth/login", json={"email": "sales@audit.com", "password": "password123"}, headers={"x-bypass-rate-limit": "true"}).json()
        sales_token = sales_login["token"]

        # Register Admin
        reg_admin = client.post(f"{base_url}/auth/register", json={
            "name": "audit_admin", "email": "admin@audit.com", "password": "password123", "role": "Admin"
        }, headers={"x-bypass-rate-limit": "true"})
        admin_tok_val = reg_admin.json().get("verification_token")
        client.post(f"{base_url}/auth/verify-email", json={"token": admin_tok_val}, headers={"x-bypass-rate-limit": "true"})
        
        print("Admin Register Status:", reg_admin.status_code, reg_admin.text)
        admin_login_res = client.post(f"{base_url}/auth/login", json={"email": "admin@audit.com", "password": "password123"}, headers={"x-bypass-rate-limit": "true"})
        print("Admin Login Status:", admin_login_res.status_code, admin_login_res.text)
        admin_login = admin_login_res.json()
        admin_token = admin_login.get("token")

    invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalidtoken.signature"

    # Define our 11 key security endpoints to audit
    # Each item has: (name, path, method, payload, allowed_roles, blocked_roles_tokens_dict)
    # The dictionary maps: token_name -> (token_value, expected_status)
    endpoints = [
        {
            "name": "Invoice Creation",
            "path": "/api/invoices",
            "method": "POST",
            "payload": {
                "invoice_number": "INV-AUD-01", "customer_id": 1, "store_id": 1,
                "subtotal": 100.0, "discount_amount": 0.0, "tax_amount": 5.0, "total_amount": 105.0,
                "payment_status": "Unpaid", "items": [{"product_id": 1, "quantity": 1, "unit_price": 100.0, "line_total": 100.0}]
            },
            "cases": {
                "No Token": (None, 401),
                "Invalid Token": (invalid_token, 401),
                "Sales Exec": (sales_token, 200),
                "Owner": (owner_token, 200),
                "Admin": (admin_token, 403)
            }
        },
        {
            "name": "Update Invoice Status",
            "path": "/api/invoices/1/status",
            "method": "PUT",
            "payload": {"payment_status": "Paid"},
            "cases": {
                "No Token": (None, 401),
                "Invalid Token": (invalid_token, 401),
                "Sales Exec": (sales_token, 403),
                "Owner": (owner_token, 200),
                "Admin": (admin_token, 403)
            }
        },
        {
            "name": "Bulk Invoice Update",
            "path": "/api/invoices/bulk-update",
            "method": "POST",
            "payload": {"invoice_ids": [1, 2], "status": "Paid"},
            "cases": {
                "No Token": (None, 401),
                "Invalid Token": (invalid_token, 401),
                "Sales Exec": (sales_token, 403),
                "Owner": (owner_token, 200),
                "Admin": (admin_token, 403)
            }
        },
        {
            "name": "Revenue Summary",
            "path": "/api/invoices/revenue-summary",
            "method": "GET",
            "payload": None,
            "cases": {
                "No Token": (None, 401),
                "Invalid Token": (invalid_token, 401),
                "Sales Exec": (sales_token, 403),
                "Owner": (owner_token, 200),
                "Admin": (admin_token, 403)
            }
        },
        {
            "name": "Inventory Update",
            "path": "/api/inventory/update",
            "method": "POST",
            "payload": {"product_id": "1", "stock_quantity": 50},
            "cases": {
                "No Token": (None, 401),
                "Invalid Token": (invalid_token, 401),
                "Sales Exec": (sales_token, 403),
                "Owner": (owner_token, 200),
                "Admin": (admin_token, 403)
            }
        },
        {
            "name": "Bulk Inventory Update",
            "path": "/api/inventory/bulk-update",
            "method": "POST",
            "payload": {"updates": [{"product_id": 1, "stock_quantity": 50}]},
            "cases": {
                "No Token": (None, 401),
                "Invalid Token": (invalid_token, 401),
                "Sales Exec": (sales_token, 403),
                "Owner": (owner_token, 200),
                "Admin": (admin_token, 403)
            }
        },
        {
            "name": "System Alerts Notifications",
            "path": "/api/notifications",
            "method": "GET",
            "payload": None,
            "cases": {
                "No Token": (None, 401),
                "Invalid Token": (invalid_token, 401),
                "Sales Exec": (sales_token, 403),
                "Owner": (owner_token, 200),
                "Admin": (admin_token, 403)
            }
        },
        {
            "name": "Audit summary",
            "path": "/api/admin/audit-summary",
            "method": "GET",
            "payload": None,
            "cases": {
                "No Token": (None, 401),
                "Invalid Token": (invalid_token, 401),
                "Sales Exec": (sales_token, 403),
                "Owner": (owner_token, 200),
                "Admin": (admin_token, 200)
            }
        },
        {
            "name": "AI Segmentation Report",
            "path": "/api/ai/segmentation",
            "method": "GET",
            "payload": None,
            "cases": {
                "No Token": (None, 401),
                "Invalid Token": (invalid_token, 401),
                "Sales Exec": (sales_token, 403),
                "Owner": (owner_token, 200),
                "Admin": (admin_token, 403)
            }
        },
        {
            "name": "AI Churn Analysis",
            "path": "/api/ai/churn",
            "method": "GET",
            "payload": None,
            "cases": {
                "No Token": (None, 401),
                "Invalid Token": (invalid_token, 401),
                "Sales Exec": (sales_token, 403),
                "Owner": (owner_token, 200),
                "Admin": (admin_token, 403)
            }
        },
        {
            "name": "AI Product Recommendation",
            "path": "/api/ai/recommendation",
            "method": "GET",
            "payload": None,
            "cases": {
                "No Token": (None, 401),
                "Invalid Token": (invalid_token, 401),
                "Sales Exec": (sales_token, 200),
                "Owner": (owner_token, 200),
                "Admin": (admin_token, 403)
            }
        }
    ]

    passed_checks = 0
    total_checks = 0

    with httpx.Client() as client:
        for ep in endpoints:
            print(f"Checking Endpoint: {ep['name']} ({ep['method']} {ep['path']})")
            for profile_name, (token, expected_status) in ep["cases"].items():
                total_checks += 1
                headers = {}
                if token:
                    headers["Authorization"] = f"Bearer {token}"
                
                # Make HTTP call
                try:
                    if ep["method"] == "GET":
                        res = client.get(f"{base_url}{ep['path']}", headers=headers)
                    elif ep["method"] == "POST":
                        res = client.post(f"{base_url}{ep['path']}", json=ep["payload"], headers=headers)
                    elif ep["method"] == "PUT":
                        res = client.put(f"{base_url}{ep['path']}", json=ep["payload"], headers=headers)
                    
                    status_code = res.status_code
                except Exception as e:
                    print(f"  [ERROR] Request to {ep['path']} failed: {e}")
                    status_code = 500

                if status_code == expected_status:
                    print(f"  [PASS] Profile '{profile_name}': Code {status_code} matched expected.")
                    passed_checks += 1
                else:
                    print(f"  [FAIL] Profile '{profile_name}': Expected {expected_status}, got {status_code}!")
            print("-" * 50)

    # Summary and final assertions
    print("\n======================================================================")
    print("AUDIT RESULTS SUMMARY")
    print(f"Passed Checks: {passed_checks} / {total_checks}")
    print("======================================================================")

    # Cleanup subprocesses
    print("Stopping API Gateway server...")
    server_process.terminate()
    server_process.wait()

    if passed_checks != total_checks:
        print("[FAIL] Security Audit scanner found validation gaps!")
        sys.exit(1)
    else:
        print("[PASS] All security constraints validated successfully!")
        sys.exit(0)

if __name__ == "__main__":
    run_security_audit()
