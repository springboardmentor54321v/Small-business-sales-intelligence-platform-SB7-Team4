# Security & Authentication Strategy (Milestone 1)

This document outlines the authentication protocol, JWT claims structure, and the Role-Based Access Control (RBAC) permission matrix designed for the MarketMind AI platform.

---

## 1. Authentication Strategy

MarketMind AI uses a **stateless, token-based authentication** architecture utilizing **JSON Web Tokens (JWT)**.

- **Token Provider**: The API Gateway (`gateway`) handles user credentials checking, hashing verification (using Python `bcrypt`), and token generation.
- **Bearer Authentication**: Clients must present the JWT in the HTTP headers of all protected requests:
  ```http
  Authorization: Bearer <JWT_TOKEN>
  ```
- **Lifecycle**: Access tokens are valid for **15 minutes** by default and refresh tokens are valid for **7 days**.

---

## 2. JWT Payload Structure

The JWT claims payload contains the user's primary identity and role, allowing downstream services to perform context-specific actions without re-querying user data:

```json
{
  "userId": 102,
  "name": "johndoe",
  "role": "Store Manager",
  "iat": 1718012345,
  "exp": 1718098745
}
```

- `userId` (Int): Unique database identifier of the user.
- `name` (String): Display name of the user, matching `users.name` in the database.
- `role` (String): Literal name of the user role, matching the database `Role` tables.
- `iat` / `exp`: Issue and expiration unix epoch timestamps.

---

## 3. Role-Based Access Control (RBAC) Matrix

The table below outlines the endpoint permissions for each module:

| Route Path | Description | HTTP Method | Permitted Roles |
| :--- | :--- | :--- | :--- |
| `/auth/register` | User Registration | POST | **Public** (Anyone) |
| `/auth/login` | User Credentials Login | POST | **Public** (Anyone) |
| `/api/sales/upload` | CSV Sales File Ingestion | POST | `Business Owner`, `Store Manager`, `Sales Executive` |
| `/api/sales/dashboard-metrics` | Aggregated Analytics Charts | GET | `Business Owner`, `Store Manager` |
| `/api/inventory` | List Products & Stock Counts | GET | `Business Owner`, `Store Manager`, `Sales Executive` |
| `/api/inventory/update` | Add/Update Stock & Thresholds | POST | `Business Owner`, `Store Manager` |
| `/api/forecast/sample` | AI Forecasting Stub Predictor | GET | `Business Owner` |
| `/api/audit-logs` | Admin System Activity Tracking | GET | `System Administrator` |

---

## 4. API Gateway Proxy Flow

When a client sends a request to a protected endpoint:
1. **Extraction**: The API Gateway extracts the token from the `Authorization: Bearer <token>` header.
2. **Signature Verification**: The token is decoded and validated against a shared environment key (`JWT_SECRET`).
3. **Role Validation**: The gateway checks the `role` property in the token payload against the routing permissions rules.
4. **Header Injection**: If authorized, the gateway proxies the request to the target microservice (e.g. `backend` or `ai` engine) and injects identity headers to inform downstream layers:
   - `x-user-id`: The verified `userId` (downstream services use this to populate `created_by_user_id` on transaction updates)
   - `x-user-role`: The verified `role`
5. **Denial**: If unauthorized, the gateway returns a `401 Unauthorized` or `403 Forbidden` response and records the rejection in the audit logs.
