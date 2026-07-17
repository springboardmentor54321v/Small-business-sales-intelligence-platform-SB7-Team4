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

---

## 5. Milestone 2 Access Rules (Day 1 Work)

The planning phase of Milestone 2 expands the Role-Based Access Control (RBAC) coverage to secure the newly introduced Invoices and AI-Powered Forecasting/Analytics endpoints. Below are the access rule definitions defined in plain, layman-friendly terms:

* **Invoices Management**:
  * **Create Invoice**: Allows recording a new sale. Permitted to **Sales Executives**, **Store Managers**, and **Business Owners** (since any of these roles can handle a transaction at the counter).
  * **View/List Invoices**: Allows viewing and searching invoices by customer name, status, or invoice number. Permitted to **Sales Executives**, **Store Managers**, and **Business Owners** to track outstanding payments and client history.
  * **Update Payment Status**: Allows marking an invoice as "Paid" or "Partially Paid". Restrictive administrative access is granted only to **Store Managers** and **Business Owners** to prevent unauthorized financial edits at the counter.
  * **Revenue & Outstanding Summary**: Provides a high-level summary of total revenue, outstanding collection amounts, and daily collections. Restrictive access is granted to **Store Managers** and **Business Owners**.
* **AI Analytics Reports**:
  * **Customer Segmentation (Customer Insights)**: Clusters customers into Loyal, Occasional, or High-Value groups. Permitted only to the **Business Owner** for high-level marketing strategy.
  * **Churn Risk Check**: Identifies customer accounts showing signs of inactivity or risk of churn. Permitted to **Store Managers** and **Business Owners** to execute retention programs.
  * **Product Recommendations**: Analyzes products frequently bought together to assist with cross-selling. Open to **Sales Executives**, **Store Managers**, and **Business Owners** to facilitate active recommendations at the point of sale.
  * **Anomaly Detection (Alerts)**: Identifies outlier sales transactions or anomalous stock changes. Restrictive access is granted to **Store Managers** and **Business Owners** to alert management to suspicious store activities.

---

## 6. Milestone 2 Permission Matrix (Day 2 Work)

This table represents the comprehensive role-permission mapping matrix for the new Milestone 2 endpoints. System Administrators remain restricted from accessing direct business financial records or sales predictions to respect administrative separation of duties.

| Feature / Action | Proposed Gateway Route | Business Owner | Store Manager | Sales Executive | System Administrator |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Create Invoice** | `POST /api/invoices` | ✅ | ✅ | ✅ | ❌ |
| **View/List Invoices** | `GET /api/invoices` | ✅ | ✅ | ✅ | ❌ |
| **Update Payment Status** | `PUT /api/invoices/{id}/status` | ✅ | ✅ | ❌ | ❌ |
| **Revenue Summary API** | `GET /api/invoices/revenue-summary` | ✅ | ✅ | ❌ | ❌ |
| **Customer Segmentation** | `GET /api/ai/segmentation` | ✅ | ❌ | ❌ | ❌ |
| **Churn Risk Flagging** | `GET /api/ai/churn` | ✅ | ✅ | ❌ | ❌ |
| **Product Recommendation** | `GET /api/ai/recommendation` | ✅ | ✅ | ✅ | ❌ |
| **Anomaly Detection** | `GET /api/ai/anomaly` | ✅ | ✅ | ❌ | ❌ |
