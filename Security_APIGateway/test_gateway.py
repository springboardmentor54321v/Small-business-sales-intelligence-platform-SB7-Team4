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

            print("\n===========================================")
            print("All 18 API Gateway integration tests passed successfully!")
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
