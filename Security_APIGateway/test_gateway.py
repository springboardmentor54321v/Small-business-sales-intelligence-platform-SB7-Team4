import subprocess
import time
import os
import sys
import httpx

def run_tests():
    print("Starting API Gateway test suite in Python...")
    
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

            print("\n===========================================")
            print("All 11 API Gateway integration tests passed successfully!")
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
