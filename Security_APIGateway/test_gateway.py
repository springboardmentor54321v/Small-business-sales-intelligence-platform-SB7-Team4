# pyrefly: ignore-file
# type: ignore
import subprocess
import time
import os

import sys
import httpx
import threading
import uvicorn
from fastapi import FastAPI, Header

# Spin up a mock backend on Port 8000 to test reverse proxy routing
mock_backend = FastAPI()

@mock_backend.get("/inventory/")
def mock_inventory(x_user_id: str = Header(None), x_user_role: str = Header(None)):
    return {
        "message": "Mock Inventory forward success",
        "injected_user_id": x_user_id,
        "injected_user_role": x_user_role
    }

@mock_backend.put("/inventory/{product_id}")
def mock_inventory_update(product_id: str, payload: dict, x_user_id: str = Header(None), x_user_role: str = Header(None)):
    return {
        "message": "Mock Inventory update forward success",
        "product_id": product_id,
        "payload": payload,
        "injected_user_id": x_user_id,
        "injected_user_role": x_user_role
    }

@mock_backend.post("/api/sales/upload")
def mock_sales_upload(x_user_id: str = Header(None), x_user_role: str = Header(None)):
    return {
        "message": "Mock Sales upload forward success",
        "injected_user_id": x_user_id,
        "injected_user_role": x_user_role
    }

@mock_backend.post("/api/invoices")
def mock_create_invoice(payload: dict, x_user_id: str = Header(None), x_user_role: str = Header(None)):
    return {
        "message": "Mock Create Invoice forward success",
        "invoice_number": payload.get("invoice_number"),
        "customer_name": payload.get("customer_name"),
        "total_amount": payload.get("total_amount"),
        "payment_status": payload.get("payment_status"),
        "injected_user_id": x_user_id,
        "injected_user_role": x_user_role
    }

@mock_backend.get("/api/invoices")
def mock_list_invoices(x_user_id: str = Header(None), x_user_role: str = Header(None)):
    return {
        "message": "Mock List Invoices forward success",
        "invoices": [
            {"id": 1, "invoice_number": "INV-001", "customer_name": "John Doe", "total_amount": 150.0, "payment_status": "Paid"}
        ],
        "injected_user_id": x_user_id,
        "injected_user_role": x_user_role
    }

@mock_backend.put("/api/invoices/{id}/status")
def mock_update_invoice_status(id: int, payload: dict, x_user_id: str = Header(None), x_user_role: str = Header(None)):
    return {
        "message": "Mock Update Invoice Status forward success",
        "invoice_id": id,
        "payment_status": payload.get("payment_status"),
        "injected_user_id": x_user_id,
        "injected_user_role": x_user_role
    }

@mock_backend.get("/api/invoices/revenue-summary")
def mock_revenue_summary(x_user_id: str = Header(None), x_user_role: str = Header(None)):
    return {
        "message": "Mock Revenue Summary forward success",
        "total_revenue": 1000.0,
        "total_outstanding": 500.0,
        "daily_collections": 500.0,
        "injected_user_id": x_user_id,
        "injected_user_role": x_user_role
    }

@mock_backend.post("/invoices/bulk-update")
def mock_invoices_bulk_update(payload: dict, x_user_id: str = Header(None), x_user_role: str = Header(None)):
    return {
        "message": "Mock Invoices Bulk Update forward success",
        "injected_user_id": x_user_id,
        "injected_user_role": x_user_role
    }

@mock_backend.post("/inventory/bulk-update")
def mock_inventory_bulk_update(payload: dict, x_user_id: str = Header(None), x_user_role: str = Header(None)):
    return {
        "message": "Mock Inventory Bulk Update forward success",
        "injected_user_id": x_user_id,
        "injected_user_role": x_user_role
    }

def run_mock_backend():
    uvicorn.run(mock_backend, host="127.0.0.1", port=8000, log_level="warning")

def run_tests():
    print("Starting API Gateway test suite in Python...")
    
    # Spawn Mock Backend server on Port 8000 in a background thread
    backend_thread = threading.Thread(target=run_mock_backend, daemon=True)
    backend_thread.start()
    time.sleep(1) # wait for mock backend to start
    
    # 1. Spawn FastAPI server as a child process
    server_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "server:app", "--port", "5000"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Wait for server to bind and start listening
    started = False
    for _ in range(30):
        # We can read line by line or wait a bit
        time.sleep(0.5)
        # Check if process is still running
        if server_process.poll() is not None:
            print("Server process exited prematurely.")
            break
        
        # Test connection
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

    print("\nServer started successfully. Beginning test requests...")
    base_url = "http://localhost:5000"
    owner_token = ""
    sales_token = ""

    try:
        with httpx.Client() as client:
            # Test 1: Register Business Owner
            print("\n-------------------------------------------")
            print("Test 1: Registering Business Owner...")
            reg_owner_res = client.post(
                f"{base_url}/auth/register",
                json={
                    "name": "alice_owner",
                    "email": "alice@marketmind.com",
                    "password": "password123",
                    "role": "Business Owner"
                }
            )
            print(f"Status: {reg_owner_res.status_code}")
            print(f"Response: {reg_owner_res.json()}")
            assert reg_owner_res.status_code == 201

            # Test 2: Register Sales Executive
            print("\n-------------------------------------------")
            print("Test 2: Registering Sales Executive...")
            reg_sales_res = client.post(
                f"{base_url}/auth/register",
                json={
                    "name": "bob_sales",
                    "email": "bob@marketmind.com",
                    "password": "password456",
                    "role": "Sales Executive"
                }
            )
            print(f"Status: {reg_sales_res.status_code}")
            print(f"Response: {reg_sales_res.json()}")
            assert reg_sales_res.status_code == 201

            # Test 3: Login Business Owner
            print("\n-------------------------------------------")
            print("Test 3: Logging in Business Owner...")
            login_owner_res = client.post(
                f"{base_url}/auth/login",
                json={
                    "email": "alice@marketmind.com",
                    "password": "password123"
                }
            )
            print(f"Status: {login_owner_res.status_code}")
            login_owner_data = login_owner_res.json()
            owner_token = login_owner_data.get("token")
            owner_refresh_token = login_owner_data.get("refreshToken")
            print(f"Response Access Token Exists: {bool(owner_token)}")
            print(f"Response Refresh Token Exists: {bool(owner_refresh_token)}")
            assert login_owner_res.status_code == 200
            assert owner_token is not None
            assert owner_refresh_token is not None

            # Test 4: Login Sales Executive
            print("\n-------------------------------------------")
            print("Test 4: Logging in Sales Executive...")
            login_sales_res = client.post(
                f"{base_url}/auth/login",
                json={
                    "email": "bob@marketmind.com",
                    "password": "password456"
                }
            )
            print(f"Status: {login_sales_res.status_code}")
            login_sales_data = login_sales_res.json()
            sales_token = login_sales_data.get("token")
            sales_refresh_token = login_sales_data.get("refreshToken")
            print(f"Response Access Token Exists: {bool(sales_token)}")
            print(f"Response Refresh Token Exists: {bool(sales_refresh_token)}")
            assert login_sales_res.status_code == 200
            assert sales_token is not None
            assert sales_refresh_token is not None

            # Test 4b: Testing login with invalid password (Should fail 401)
            print("\n-------------------------------------------")
            print("Test 4b: Testing login with invalid password...")
            bad_login_res = client.post(
                f"{base_url}/auth/login",
                json={"email": "alice@marketmind.com", "password": "wrong_password_123"}
            )
            print(f"Status: {bad_login_res.status_code} (Expected: 401)")
            assert bad_login_res.status_code == 401
            assert bad_login_res.json().get("detail") == "Invalid credentials"

            # Test 5: Access Forecasting as Business Owner (Permitted)

            print("\n-------------------------------------------")
            print("Test 5: Accessing /api/forecast/sample as Business Owner (Permitted)...")
            forecast_owner_res = client.get(
                f"{base_url}/api/forecast/sample",
                headers={"Authorization": f"Bearer {owner_token}"}
            )
            print(f"Status: {forecast_owner_res.status_code}")
            print(f"Response: {forecast_owner_res.json()}")
            assert forecast_owner_res.status_code == 200

            # Test 6: Access Forecasting as Sales Executive (Blocked)
            print("\n-------------------------------------------")
            print("Test 6: Accessing /api/forecast/sample as Sales Executive (Blocked)...")
            forecast_sales_res = client.get(
                f"{base_url}/api/forecast/sample",
                headers={"Authorization": f"Bearer {sales_token}"}
            )
            print(f"Status: {forecast_sales_res.status_code} (Expected: 403)")
            print(f"Response: {forecast_sales_res.json()}")
            assert forecast_sales_res.status_code == 403

            # Test 7: Access Forecasting with no Token (Blocked)
            print("\n-------------------------------------------")
            print("Test 7: Accessing /api/forecast/sample with no token (Blocked)...")
            forecast_no_token_res = client.get(f"{base_url}/api/forecast/sample")
            print(f"Status: {forecast_no_token_res.status_code} (Expected: 401)")
            print(f"Response: {forecast_no_token_res.json()}")
            assert forecast_no_token_res.status_code == 401

            # Test 8: Refresh Token Rotation
            print("\n-------------------------------------------")
            print("Test 8: Rotating Access Token using Refresh Token...")
            time.sleep(1)  # Sleep 1s to ensure token timestamps differ
            refresh_res = client.post(
                f"{base_url}/auth/refresh",
                json={"refresh_token": owner_refresh_token}
            )
            print(f"Status: {refresh_res.status_code}")
            refresh_data = refresh_res.json()
            new_access_token = refresh_data.get("token")
            print(f"New Access Token Exists: {bool(new_access_token)}")
            assert refresh_res.status_code == 200
            assert new_access_token is not None
            assert new_access_token != owner_token

            # Test 9: Refresh with Invalid Token
            print("\n-------------------------------------------")
            print("Test 9: Refreshing with Invalid/Malformed Token...")
            refresh_invalid_res = client.post(
                f"{base_url}/auth/refresh",
                json={"refresh_token": "invalid-token-value"}
            )
            print(f"Status: {refresh_invalid_res.status_code} (Expected: 401)")
            print(f"Response: {refresh_invalid_res.json()}")
            assert refresh_invalid_res.status_code == 401

            # Test 10: Revoke Tokens on Logout
            print("\n-------------------------------------------")
            print("Test 10: Logging out and revoking refresh tokens...")
            logout_res = client.post(
                f"{base_url}/auth/logout",
                headers={"Authorization": f"Bearer {new_access_token}"}
            )
            print(f"Status: {logout_res.status_code}")
            print(f"Response: {logout_res.json()}")
            assert logout_res.status_code == 200

            # Verify that refresh token is now revoked
            print("\n-------------------------------------------")
            print("Test 11 (Verification): Refreshing with revoked token (Should fail)...")
            refresh_revoked_res = client.post(
                f"{base_url}/auth/refresh",
                json={"refresh_token": owner_refresh_token}
            )
            print(f"Status: {refresh_revoked_res.status_code} (Expected: 401)")
            print(f"Response: {refresh_revoked_res.json()}")
            assert refresh_revoked_res.status_code == 401

            # Log in Alice again to get a fresh token for admin operations
            print("\n-------------------------------------------")
            print("Logging Alice back in to perform admin/manager proxy tasks...")
            login_again_res = client.post(
                f"{base_url}/auth/login",
                json={
                    "email": "alice@marketmind.com",
                    "password": "password123"
                }
            )
            assert login_again_res.status_code == 200
            alice_new_token = login_again_res.json().get("token")
            print("New Access Token acquired for Alice.")

            # Test 12: Reverse Proxy Routing & Header Injection
            print("\n-------------------------------------------")
            print("Test 12: Accessing /api/inventory via Gateway (Proxy forward & Header injection)...")
            proxy_res = client.get(
                f"{base_url}/api/inventory",
                headers={"Authorization": f"Bearer {sales_token}"}
            )
            print(f"Status: {proxy_res.status_code}")
            proxy_data = proxy_res.json()
            print(f"Response: {proxy_data}")
            assert proxy_res.status_code == 200
            assert proxy_data.get("message") == "Mock Inventory forward success"
            assert proxy_data.get("injected_user_id") == "2"
            assert proxy_data.get("injected_user_role") == "Sales Executive"

            # Test 13: Schema Validation Rejection
            print("\n-------------------------------------------")
            print("Test 13: Testing Schema Validation with missing fields (Should fail 422)...")
            malformed_payload = {"stock_quantity": 100} # missing product_id
            validation_res = client.post(
                f"{base_url}/api/inventory/update",
                json=malformed_payload,
                headers={"Authorization": f"Bearer {alice_new_token}"}
            )
            print(f"Status: {validation_res.status_code} (Expected: 422)")
            print(f"Response: {validation_res.json()}")
            assert validation_res.status_code == 422

            # Test 14: Ingestion MIME-Type Block
            print("\n-------------------------------------------")
            print("Test 14: Uploading non-CSV file (Should fail 400)...")
            txt_files = {"file": ("test.txt", b"plain text content", "text/plain")}
            upload_res = client.post(
                f"{base_url}/api/sales/upload",
                files=txt_files,
                headers={"Authorization": f"Bearer {alice_new_token}"}
            )
            print(f"Status: {upload_res.status_code} (Expected: 400)")
            print(f"Response: {upload_res.json()}")
            assert upload_res.status_code == 400

            # Test 15: Valid CSV Ingestion Forwarding
            print("\n-------------------------------------------")
            print("Test 15: Uploading valid CSV file (Should succeed)...")
            csv_files = {"file": ("sales.csv", b"invoice_id,customer_id,product_id,quantity,total_amount,transaction_date\nINV01,C01,P01,5,100.0,2026-07-10", "text/csv")}
            upload_csv_res = client.post(
                f"{base_url}/api/sales/upload",
                files=csv_files,
                headers={"Authorization": f"Bearer {alice_new_token}"}
            )
            print(f"Status: {upload_csv_res.status_code} (Expected: 200)")
            csv_data = upload_csv_res.json()
            print(f"Response: {csv_data}")
            assert upload_csv_res.status_code == 200
            assert csv_data.get("message") == "Mock Sales upload forward success"
            assert csv_data.get("injected_user_id") == "1"
            assert csv_data.get("injected_user_role") == "Business Owner"

            # Test 16: Authentication Rate Limiting
            print("\n-------------------------------------------")
            print("Test 16: Testing Authentication Rate Limiting (Should trigger HTTP 429 on 11th call)...")
            throttled = False
            for i in range(11):
                rate_res = client.post(
                    f"{base_url}/auth/login",
                    json={
                        "email": "alice@marketmind.com",
                        "password": "password123"
                    }
                )
                print(f"Call {i+1} Status: {rate_res.status_code}")
                if rate_res.status_code == 429:
                    throttled = True
                    print(f"Response: {rate_res.json()}")
                    break
            assert throttled is True

            # Test 17: Testing API Path Rate Limiting
            print("\n-------------------------------------------")
            print("Test 17: Testing API Path Rate Limiting (Should trigger HTTP 429 on 4th call)...")
            api_throttled = False
            for i in range(4):
                rate_res = client.get(
                    f"{base_url}/api/test-rate-limit",
                    headers={"Authorization": f"Bearer {sales_token}"}
                )
                print(f"Call {i+1} Status: {rate_res.status_code}")
                if rate_res.status_code == 429:
                    api_throttled = True
                    print(f"Response: {rate_res.json()}")
                    break
            assert api_throttled is True

            # Test 18: Persistent Audit Log Verification
            print("\n-------------------------------------------")
            print("Test 18: Verifying persistent audit.log creation and contents...")
            log_path = os.path.join(os.path.dirname(__file__), "audit.log")
            assert os.path.exists(log_path) is True
            with open(log_path, "r", encoding="utf-8") as f:
                logs = f.read()
            assert " - [INFO] - User Registered" in logs or " - [INFO] - User Logged In" in logs
            assert "rate limit exceeded" in logs or "rate limit triggered" in logs
            print("Log file verified successfully. Last 5 entries:")
            print("\n".join(logs.splitlines()[-5:]))

            # Test 19: Create Invoice (Sales Executive - Permitted)
            print("\n-------------------------------------------")
            print("Test 19: Creating Invoice as Sales Executive...")
            invoice_payload = {
                "invoice_number": "INV-M2-01",
                "customer_id": 1,
                "store_id": 1,
                "subtotal": 100.0,
                "discount_amount": 5.0,
                "tax_amount": 10.0,
                "total_amount": 105.0,
                "payment_status": "Unpaid",
                "invoice_status": "Active",
                "notes": "Test invoice",
                "items": [
                    {
                        "product_id": 1,
                        "quantity": 2,
                        "unit_price": 50.0,
                        "discount": 2.5,
                        "tax": 5.0,
                        "line_total": 102.5,
                        "category_snapshot": "Electronics",
                        "product_name_snapshot": "Wireless Headphones"
                    }
                ]

            }
            create_inv_res = client.post(
                f"{base_url}/api/invoices",
                json=invoice_payload,
                headers={"Authorization": f"Bearer {sales_token}"}
            )
            print(f"Status: {create_inv_res.status_code} (Expected: 200)")
            inv_data = create_inv_res.json()
            print(f"Response: {inv_data}")
            assert create_inv_res.status_code == 200
            assert "success" in inv_data.get("message").lower()
            assert inv_data.get("invoice_number") == "INV-M2-01"


            # Test 20: Create Invoice Schema Validation Failure (Should fail with 422)
            print("\n-------------------------------------------")
            print("Test 20: Rejections on malformed/negative invoice data...")
            
            # Case A: Negative unit price
            import copy
            bad_payload_1 = copy.deepcopy(invoice_payload)
            bad_payload_1["items"][0]["unit_price"] = -5.0
            res_bad_1 = client.post(
                f"{base_url}/api/invoices",
                json=bad_payload_1,
                headers={"Authorization": f"Bearer {sales_token}"}
            )
            print(f"Case A (Negative unit_price) Status: {res_bad_1.status_code} (Expected: 422)")
            assert res_bad_1.status_code == 422

            # Case B: Invalid payment status value
            bad_payload_2 = dict(invoice_payload)
            bad_payload_2["payment_status"] = "SuperPaid"
            res_bad_2 = client.post(
                f"{base_url}/api/invoices",
                json=bad_payload_2,
                headers={"Authorization": f"Bearer {sales_token}"}
            )
            print(f"Case B (Invalid payment_status) Status: {res_bad_2.status_code} (Expected: 422)")
            assert res_bad_2.status_code == 422

            # Test 21: Update Invoice Payment Status RBAC (Store Manager vs Sales Executive)
            print("\n-------------------------------------------")
            print("Test 21: Update Invoice Payment Status RBAC check...")
            
            # Sales Executive (bob_sales) should be blocked (403 Forbidden)
            status_payload = {"payment_status": "Paid"}
            update_status_sales_res = client.put(
                f"{base_url}/api/invoices/1/status",
                json=status_payload,
                headers={"Authorization": f"Bearer {sales_token}"}
            )
            print(f"Sales Executive (Bob) Status: {update_status_sales_res.status_code} (Expected: 403)")
            assert update_status_sales_res.status_code == 403

            # Business Owner (Alice) should be allowed (200 OK)
            update_status_owner_res = client.put(
                f"{base_url}/api/invoices/1/status",
                json=status_payload,
                headers={"Authorization": f"Bearer {alice_new_token}"}
            )
            print(f"Business Owner (Alice) Status: {update_status_owner_res.status_code} (Expected: 200)")
            assert update_status_owner_res.status_code == 200

            # Test 22: AI Analytics Endpoints RBAC (Business Owner vs Store Manager / Sales Executive)
            print("\n-------------------------------------------")
            print("Test 22: AI Customer Segmentation Endpoint access check...")
            
            # Sales Executive (Bob) is blocked (403)
            segment_sales_res = client.get(
                f"{base_url}/api/ai/segmentation",
                headers={"Authorization": f"Bearer {sales_token}"}
            )
            print(f"Sales Executive Status: {segment_sales_res.status_code} (Expected: 403)")
            assert segment_sales_res.status_code == 403

            # Business Owner (Alice) is permitted (200)
            segment_owner_res = client.get(
                f"{base_url}/api/ai/segmentation",
                headers={"Authorization": f"Bearer {alice_new_token}"}
            )
            print(f"Business Owner Status: {segment_owner_res.status_code} (Expected: 200)")
            assert segment_owner_res.status_code == 200
            assert "segments" in segment_owner_res.json()

            # Test 24: AI Churn, Recommendation, and Anomaly RBAC verification
            print("\n-------------------------------------------")
            print("Test 24: Testing AI Churn, Recommendation, and Anomaly RBAC rules...")
            
            # AI Churn Risk (Business Owner & Store Manager permitted, Sales Executive blocked)
            churn_sales_res = client.get(
                f"{base_url}/api/ai/churn",
                headers={"Authorization": f"Bearer {sales_token}"}
            )
            print(f"AI Churn (Sales Executive) Status: {churn_sales_res.status_code} (Expected: 403)")
            assert churn_sales_res.status_code == 403

            churn_owner_res = client.get(
                f"{base_url}/api/ai/churn",
                headers={"Authorization": f"Bearer {alice_new_token}"}
            )
            print(f"AI Churn (Business Owner) Status: {churn_owner_res.status_code} (Expected: 200)")
            assert churn_owner_res.status_code == 200

            # AI Recommendations (Sales Executive permitted)
            rec_sales_res = client.get(
                f"{base_url}/api/ai/recommendation",
                headers={"Authorization": f"Bearer {sales_token}"}
            )
            print(f"AI Recommendation (Sales Executive) Status: {rec_sales_res.status_code} (Expected: 200)")
            assert rec_sales_res.status_code == 200

            # AI Anomaly Detection (Sales Executive blocked)
            anomaly_sales_res = client.get(
                f"{base_url}/api/ai/anomaly",
                headers={"Authorization": f"Bearer {sales_token}"}
            )
            print(f"AI Anomaly (Sales Executive) Status: {anomaly_sales_res.status_code} (Expected: 403)")
            assert anomaly_sales_res.status_code == 403

            # Test 26: Milestone 3 Day 2 - Notifications and Bulk Update APIs RBAC Validation
            print("\n-------------------------------------------")
            print("Test 26: Testing Notifications & Bulk Update APIs RBAC rules...")
            
            # Notifications (Business Owner permitted, Sales Executive blocked)
            notif_sales_res = client.get(
                f"{base_url}/api/notifications",
                headers={"Authorization": f"Bearer {sales_token}"}
            )
            print(f"Notifications (Sales Executive) Status: {notif_sales_res.status_code} (Expected: 403)")
            assert notif_sales_res.status_code == 403
            
            notif_owner_res = client.get(
                f"{base_url}/api/notifications",
                headers={"Authorization": f"Bearer {alice_new_token}"}
            )
            print(f"Notifications (Business Owner) Status: {notif_owner_res.status_code} (Expected: 200)")
            assert notif_owner_res.status_code == 200
            
            # Bulk Invoice Update (Business Owner permitted, Sales Executive blocked)
            bulk_inv_sales_res = client.post(
                f"{base_url}/api/invoices/bulk-update",
                json={"invoice_ids": [1, 2], "status": "Paid"},
                headers={"Authorization": f"Bearer {sales_token}"}
            )
            print(f"Bulk Invoice Update (Sales Executive) Status: {bulk_inv_sales_res.status_code} (Expected: 403)")
            assert bulk_inv_sales_res.status_code == 403
            
            bulk_inv_owner_res = client.post(
                f"{base_url}/api/invoices/bulk-update",
                json={"invoice_ids": [1, 2], "status": "Paid"},
                headers={"Authorization": f"Bearer {alice_new_token}"}
            )
            print(f"Bulk Invoice Update (Business Owner) Status: {bulk_inv_owner_res.status_code} (Expected: 200)")
            assert bulk_inv_owner_res.status_code == 200
            
            # Bulk Inventory Update (Business Owner permitted, Sales Executive blocked)
            bulk_item_sales_res = client.post(
                f"{base_url}/api/inventory/bulk-update",
                json={"updates": [{"product_id": 1, "stock_quantity": 20}]},
                headers={"Authorization": f"Bearer {sales_token}"}
            )
            print(f"Bulk Inventory Update (Sales Executive) Status: {bulk_item_sales_res.status_code} (Expected: 403)")
            assert bulk_item_sales_res.status_code == 403
            
            bulk_item_owner_res = client.post(
                f"{base_url}/api/inventory/bulk-update",
                json={"updates": [{"product_id": 1, "stock_quantity": 20}]},
                headers={"Authorization": f"Bearer {alice_new_token}"}
            )
            print(f"Bulk Inventory Update (Business Owner) Status: {bulk_item_owner_res.status_code} (Expected: 200)")
            assert bulk_item_owner_res.status_code == 200

            # Test 25: Verification of audit logging for invoice and AI reports
            print("\n-------------------------------------------")
            print("Test 25: Verifying audit logging records all activity...")
            with open(log_path, "r", encoding="utf-8") as f:
                logs_after = f.read()
            assert "attempted to create invoice" in logs_after
            assert "requested AI Customer Segmentation report" in logs_after
            assert "updated invoice ID 1 status" in logs_after
            print("Audit log contains complete security records!")

            # Test 27: Milestone 3 Day 3 - Audit Summary API Validation
            print("\n-------------------------------------------")
            print("Test 27: Testing Audit Summary API access & output content...")
            
            # Request audit summary as Sales Executive (should be blocked)
            summary_sales_res = client.get(
                f"{base_url}/api/admin/audit-summary",
                headers={"Authorization": f"Bearer {sales_token}"}
            )
            print(f"Audit Summary (Sales Executive) Status: {summary_sales_res.status_code} (Expected: 403)")
            assert summary_sales_res.status_code == 403
            
            # Request audit summary as Business Owner (should succeed)
            summary_owner_res = client.get(
                f"{base_url}/api/admin/audit-summary",
                headers={"Authorization": f"Bearer {alice_new_token}"}
            )
            print(f"Audit Summary (Business Owner) Status: {summary_owner_res.status_code} (Expected: 200)")
            assert summary_owner_res.status_code == 200
            
            summary_data = summary_owner_res.json()
            print("Total logs analyzed:", summary_data.get("total_logs"))
            assert "total_logs" in summary_data
            assert "user_counts" in summary_data
            assert "action_counts" in summary_data
            assert "recent_activities" in summary_data
            assert summary_data["total_logs"] > 0

            # Test 28: Milestone 3 Day 6 - Tightening validations on bulk-update endpoints
            print("\n-------------------------------------------")
            print("Test 28: Testing bulk update validation schema rejections...")
            
            # Case A: Invalid bulk invoice payload (negative invoice ID or wrong status name)
            bad_bulk_inv_res1 = client.post(
                f"{base_url}/api/invoices/bulk-update",
                json={"invoice_ids": [-1, 2], "status": "Paid"},
                headers={"Authorization": f"Bearer {alice_new_token}"}
            )
            print(f"Bulk Invoice Update (Negative ID) Status: {bad_bulk_inv_res1.status_code} (Expected: 422)")
            assert bad_bulk_inv_res1.status_code == 422

            bad_bulk_inv_res2 = client.post(
                f"{base_url}/api/invoices/bulk-update",
                json={"invoice_ids": [1, 2], "status": "SuperPaid"},
                headers={"Authorization": f"Bearer {alice_new_token}"}
            )
            print(f"Bulk Invoice Update (Invalid status name) Status: {bad_bulk_inv_res2.status_code} (Expected: 422)")
            assert bad_bulk_inv_res2.status_code == 422

            # Case B: Invalid bulk inventory update payload (negative stock quantity)
            bad_bulk_item_res = client.post(
                f"{base_url}/api/inventory/bulk-update",
                json={"updates": [{"product_id": 1, "stock_quantity": -20}]},
                headers={"Authorization": f"Bearer {alice_new_token}"}
            )
            print(f"Bulk Inventory Update (Negative quantity) Status: {bad_bulk_item_res.status_code} (Expected: 422)")
            assert bad_bulk_item_res.status_code == 422

            print("\n===========================================")
            print("All API Gateway integration tests passed successfully!")
            print("===========================================")




    except Exception as e:
        print(f"Test Suite failed: {e}")
        sys.exit(1)
    finally:
        print("Stopping API Gateway server...")
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    run_tests()
