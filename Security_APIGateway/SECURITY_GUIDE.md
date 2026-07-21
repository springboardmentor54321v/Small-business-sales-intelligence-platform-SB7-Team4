# MarketMind AI — Security & Access Guide (Milestone 2)

## 1. Overview
The **Security & API Gateway Layer** acts as the single point of entry for all incoming traffic to the MarketMind AI platform. It enforces Role-Based Access Control (RBAC), validates incoming request payloads using Pydantic schemas, logs security audit trails, enforces rate limiting, and forwards valid requests with injected identity headers (`x-user-id`, `x-user-role`) to downstream microservices.

---

## 2. Role-Based Access Control (RBAC) Matrix

| Endpoint | HTTP Method | Business Owner | Store Manager | Sales Executive | Administrator |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `/auth/register` & `/auth/login` | POST | ✅ Public | ✅ Public | ✅ Public | ✅ Public |
| `/auth/refresh` & `/auth/logout` | POST | ✅ User | ✅ User | ✅ User | ✅ User |
| `/api/invoices` (Create / View) | GET/POST | ✅ Allowed | ✅ Allowed | ✅ Allowed | ❌ Blocked |
| `/api/invoices/{id}/status` | PUT | ✅ Allowed | ✅ Allowed | ❌ Blocked | ❌ Blocked |
| `/api/sales/upload` | POST | ✅ Allowed | ✅ Allowed | ✅ Allowed | ❌ Blocked |
| `/api/inventory` | GET/POST | ✅ Allowed | ✅ Allowed | ✅ Allowed | ❌ Blocked |
| `/api/ai/segmentation` | GET | ✅ Allowed | ❌ Blocked | ❌ Blocked | ❌ Blocked |
| `/api/ai/churn` | GET | ✅ Allowed | ✅ Allowed | ❌ Blocked | ❌ Blocked |
| `/api/ai/recommendation` | GET | ✅ Allowed | ✅ Allowed | ✅ Allowed | ❌ Blocked |
| `/api/ai/anomaly` | GET | ✅ Allowed | ✅ Allowed | ❌ Blocked | ❌ Blocked |
| `/api/admin/audit-logs` | GET | ❌ Blocked | ❌ Blocked | ❌ Blocked | ✅ Allowed |

---

## 3. Security Features & Protections

### A. JWT Authentication & Token Lifecycle
* **Access Tokens**: Short-lived JWTs (15 minutes) carrying user identity (`userId`, `role`, `email`).
* **Refresh Tokens**: Cryptographically generated 64-character tokens (7 days) with automated single-use revocation on logout/rotation.

### B. Request Data Validation Schemas
* **Invoice Schemas**: Enforces database-aligned columns (`customer_id`, `store_id`, `subtotal`, `discount_amount`, `tax_amount`, `total_amount`, `payment_status`, `invoice_items`).
* Rejects malformed bodies, missing required fields, negative unit prices (`gt=0`), or invalid payment statuses (`Paid`, `Unpaid`, `Partially Paid`) returning `HTTP 422 Unprocessable Entity`.

### C. Rate Limiting (IP Throttling)
* **Auth Routes (`/auth/*`)**: Restricted to **10 requests per minute**.
* **General APIs (`/api/*`)**: Restricted to **100 requests per minute**.
* Returns `HTTP 429 Too Many Requests` when limits are exceeded.

### D. Audit Logging
* All security events (logins, failed authentication attempts, rate limit breaches, invoice creations, invoice status changes, and AI report calls) are written to persistent `audit.log` files with ISO-8601 timestamps and client IP addresses.

---

## 4. Running the Test Suite
Run the automated security integration test suite using Python:
```powershell
python Security_APIGateway/test_gateway.py
```
This launches a transient API Gateway server, executes all 25 security test scenarios end-to-end, verifies audit log generation, and cleanly terminates the server.
