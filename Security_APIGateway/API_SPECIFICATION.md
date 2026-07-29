# MarketMind AI - API Gateway Reference Specification

Welcome to the central API Specification for the MarketMind AI Small Business Sales Intelligence Platform. This API is secured at the gateway layer, enforcing Role-Based Access Control (RBAC), rate limits, and request validations.

---

## 🔑 Authentication Strategy

All secure routes require an `Authorization` header carrying a short-lived JSON Web Token (JWT):
```http
Authorization: Bearer <your_access_token>
```
* **Access Tokens**: Expire in 15 minutes.
* **Refresh Tokens**: Expire in 7 days (used to rotate access tokens).

---

## 📋 Endpoints Catalog

### 1. User & Authentication Services

#### `POST /auth/register`
* **Access**: Public
* **Request Body**:
  ```json
  {
    "username": "jane_doe",
    "email": "jane@marketmind.com",
    "password": "securepassword123",
    "role": "Sales Executive"
  }
  ```
  *Allowed roles*: `"Business Owner"`, `"Store Manager"`, `"Sales Executive"`, `"Administrator"`.
* **Response (201 Created)**:
  ```json
  {
    "message": "Registration successful",
    "user": { "id": 3, "name": "jane_doe", "email": "jane@marketmind.com", "role": "Sales Executive" }
  }
  ```

#### `POST /auth/login`
* **Access**: Public (Throttled: 10 attempts/min per IP)
* **Request Body**:
  ```json
  {
    "username": "jane_doe",
    "password": "securepassword123"
  }
  ```
* **Response (200 OK)**:
  ```json
  {
    "access_token": "eyJhbG...",
    "refresh_token": "a1b2c3d4..."
  }
  ```

#### `POST /auth/refresh`
* **Access**: Public
* **Request Body**:
  ```json
  {
    "refresh_token": "a1b2c3d4..."
  }
  ```
* **Response (200 OK)**:
  ```json
  {
    "access_token": "eyJhbG..."
  }
  ```

#### `POST /auth/logout`
* **Access**: Auth Required (All roles)
* **Response (200 OK)**:
  ```json
  {
    "message": "Logged out successfully"
  }
  ```

---

### 🧾 2. Invoice Management Services

#### `POST /api/invoices`
* **Access**: Auth Required (`Business Owner`, `Store Manager`, `Sales Executive`)
* **Request Body**:
  ```json
  {
    "invoice_number": "INV-1004",
    "customer_id": 2,
    "store_id": 1,
    "subtotal": 1200.0,
    "discount_amount": 100.0,
    "tax_amount": 99.0,
    "total_amount": 1199.0,
    "payment_status": "Unpaid",
    "items": [
      {
        "product_id": 4,
        "quantity": 2,
        "unit_price": 600.0,
        "discount": 100.0,
        "tax": 99.0,
        "line_total": 1199.0,
        "category_snapshot": "Electronics",
        "product_name_snapshot": "Monitor"
      }
    ]
  }
  ```
* **Response (200 OK)**:
  ```json
  {
    "message": "Mock Create Invoice forward success",
    "invoice_number": "INV-1004",
    "total_amount": 1199.0,
    "payment_status": "Unpaid"
  }
  ```

#### `GET /api/invoices`
* **Access**: Auth Required (`Business Owner`, `Store Manager`, `Sales Executive`)
* **Query Parameters**:
  * `payment_status` (Optional): `"Paid"`, `"Unpaid"`, `"Partially Paid"`
  * `customer_id` (Optional): Filter by customer ID number.
* **Response (200 OK)**: List of active invoices.

#### `PUT /api/invoices/{invoice_id}/status`
* **Access**: Auth Required (`Business Owner`, `Store Manager`)
* **Request Body**:
  ```json
  {
    "payment_status": "Paid"
  }
  ```
* **Response (200 OK)**: Confirms payment update.

#### `POST /api/invoices/bulk-update`
* **Access**: Auth Required (`Business Owner`, `Store Manager`)
* **Request Body**:
  ```json
  {
    "invoice_ids": [1, 2, 3],
    "status": "Paid"
  }
  ```
* **Response (200 OK)**: Confirms update status across listed identifiers.

#### `GET /api/invoices/revenue-summary`
* **Access**: Auth Required (`Business Owner`, `Store Manager`)
* **Response (200 OK)**:
  ```json
  {
    "total_revenue": 1245000.0,
    "total_outstanding": 18200.0,
    "daily_collections": 45000.0
  }
  ```

---

### 📦 3. Inventory & Sales Operations

#### `GET /api/inventory`
* **Access**: Auth Required (`Business Owner`, `Store Manager`, `Sales Executive`)
* **Response (200 OK)**: List of active inventory records.

#### `POST /api/inventory/update`
* **Access**: Auth Required (`Business Owner`, `Store Manager`)
* **Request Body**:
  ```json
  {
    "product_id": 4,
    "stock_quantity": 120,
    "low_stock_threshold": 10
  }
  ```
* **Response (200 OK)**: Confirms stock count updates.

#### `POST /api/inventory/bulk-update`
* **Access**: Auth Required (`Business Owner`, `Store Manager`)
* **Request Body**:
  ```json
  {
    "updates": [
      { "product_id": 4, "stock_quantity": 120 }
    ]
  }
  ```
* **Response (200 OK)**: Confirms bulk stock count adjustments.

#### `POST /api/sales/upload`
* **Access**: Auth Required (`Business Owner`, `Store Manager`, `Sales Executive`)
* **Request Body**: Multipart CSV file.
* **Response (200 OK)**: Confirms file parsing and database insert metrics.

---

### 🚨 4. Alerting & Administration

#### `GET /api/notifications`
* **Access**: Auth Required (`Business Owner`, `Store Manager`)
* **Response (200 OK)**:
  ```json
  [
    { "id": 1, "type": "low_stock", "message": "Product 'Mouse' is low on stock.", "created_at": "2026-07-29T12:00:00Z" }
  ]
  ```

#### `GET /api/admin/audit-summary`
* **Access**: Auth Required (`Business Owner`, `Administrator`)
* **Response (200 OK)**:
  ```json
  {
    "total_logs": 425,
    "user_counts": { "alice_owner": 240, "bob_sales": 185 },
    "action_counts": { "user_login": 32, "invoice_create_attempt": 128 },
    "recent_activities": []
  }
  ```

---

### 🤖 5. AI/ML Analytics Services

#### `POST /predict`
* **Access**: Public / Front-end integration endpoint
* **Request Body**: Multipart CSV dataset.
* **Response (200 OK)**: Array of monthly predicted sales.

#### `POST /recommend-product`
* **Access**: Public / Front-end integration endpoint
* **Request Body**:
  ```json
  {
    "Product Name": "Staples"
  }
  ```
* **Response (200 OK)**: List of recommended products.

#### `POST /check-anomaly`
* **Access**: Public / Front-end integration endpoint
* **Request Body**:
  ```json
  {
    "Order Date": "2011-01-04"
  }
  ```
* **Response (200 OK)**: Flagged anomaly events for the target date.
