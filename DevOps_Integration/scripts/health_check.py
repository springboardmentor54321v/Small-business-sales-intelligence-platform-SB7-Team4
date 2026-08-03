# pyrefly: ignore-file
# type: ignore
"""
MarketMind AI - System Health Check & Load Test Utility

DevOps Domain (Intern 5)

Usage:
  python health_check.py
"""

import time
import urllib.request
import urllib.error

SERVICES = [
    {"name": "API Security Gateway", "url": "http://localhost:5000/docs"},
    {"name": "Database Backend", "url": "http://localhost:8000/docs"},
    {"name": "AI/ML Analytics", "url": "http://localhost:5002/api/forecast/sample"},
    {"name": "Streamlit Frontend", "url": "http://localhost:8501/"},
    {"name": "Alerts & Notifications", "url": "http://localhost:5003/"}
]

def check_health():
    print("==================================================")
    print("     MarketMind AI - System Health Check         ")
    print("==================================================")
    
    online_count = 0
    for service in SERVICES:
        start_time = time.time()
        try:
            req = urllib.request.Request(service["url"], headers={"User-Agent": "HealthCheck/1.0"})
            with urllib.request.urlopen(req, timeout=3.0) as response:
                latency = (time.time() - start_time) * 1000
                print(f"[ONLINE] {service['name']:<25} | Status: {response.status} | Latency: {latency:.2f}ms")
                online_count += 1
        except urllib.error.HTTPError as e:
            latency = (time.time() - start_time) * 1000
            print(f"[ONLINE] {service['name']:<25} | Status: {e.code} | Latency: {latency:.2f}ms")
            online_count += 1
        except Exception as e:
            print(f"[OFFLINE] {service['name']:<24} | Reason: Service unreachable")

    print("--------------------------------------------------")
    print(f"Health Status: {online_count}/{len(SERVICES)} services responsive.")
    print("==================================================\n")

if __name__ == "__main__":
    check_health()
