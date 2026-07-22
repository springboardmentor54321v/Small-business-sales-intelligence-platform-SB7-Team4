# MarketMind AI Backend – API Usage Note

## Project Overview

The **MarketMind AI Backend** is developed using **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **Pydantic**. It provides REST APIs for managing sales data, inventory, invoices, payments, and revenue reporting. All APIs have been tested using **Swagger UI** and **Postman**, and the responses have been verified against the PostgreSQL database.

---

# 1. Sales Upload API

**Endpoint**

```http
POST /api/sales/upload
```

### Description

This API accepts a CSV file containing sales data. The uploaded file is validated for file type and required columns before processing. If the schema is valid, the API returns the file details and validation status; otherwise, it returns appropriate validation errors.

**Purpose**

- Initial sales data upload
- CSV validation
- Data preprocessing before database operations

---

# 2. Inventory APIs

## Endpoints

```http
GET    /inventory
GET    /inventory/{product_id}
POST   /inventory
PUT    /inventory/{product_id}
DELETE /inventory/{product_id}
```

### Description

These APIs manage product inventory. Users can retrieve all inventory records, view a single product's stock, create new inventory entries, update stock quantities, or delete inventory records. Inventory is also automatically updated whenever invoices are created.

**Purpose**

- Inventory management
- Stock monitoring
- Inventory updates after sales

---

# 3. Sales Transaction APIs

## Endpoints

```http
GET    /sales
GET    /sales/{transaction_id}
POST   /sales
PUT    /sales/{transaction_id}
DELETE /sales/{transaction_id}
```

### Description

These APIs manage sales transactions. Before recording a transaction, the backend validates available inventory and automatically reduces stock quantities after a successful sale.

Pagination has been implemented for the **GET All Sales** endpoint because the dataset contains **over 51,000 records**, improving performance and reducing response time.

**Purpose**

- Record product sales
- Update inventory
- Maintain transaction history

---

# 4. Invoice APIs

## Endpoints

```http
GET    /invoices
GET    /invoices/{invoice_id}
POST   /invoices
PUT    /invoices/{invoice_id}
DELETE /invoices/{invoice_id}
```

## Additional Filters

- `payment_status`
- `customer_id`
- `invoice_number`

### Description

Invoice creation performs the following operations automatically:

- Validates customer
- Validates store
- Validates product
- Checks inventory availability
- Generates a unique invoice number
- Calculates subtotal
- Calculates tax
- Calculates total amount
- Creates invoice items
- Updates inventory quantities

**Purpose**

Complete invoice lifecycle management.

---

# 5. Payment APIs

## Endpoints

```http
GET    /payments/{invoice_id}
POST   /payments
PUT    /payments/{payment_id}
DELETE /payments/{payment_id}
```

### Description

These APIs record and manage invoice payments. The system supports **multiple payments for a single invoice**, allowing partial payment functionality. The invoice payment status is automatically updated based on the cumulative amount received.

Possible payment statuses:

- Pending
- Partially Paid
- Paid

**Purpose**

- Payment tracking
- Invoice settlement
- Automatic payment status updates

---

# 6. Revenue Summary API

## Endpoint

```http
GET /revenue/summary
```

### Description

This API provides dashboard-level business metrics by calculating:

- Total Revenue
- Total Outstanding Amount
- Daily Collections

The returned values are calculated directly from the **Invoice** and **Payment** tables to ensure consistency with the database.

**Purpose**

Business revenue analytics and dashboard reporting.

---

# Testing Summary

The backend has been thoroughly tested using:

- Swagger UI
- Postman
- PostgreSQL database verification

## Verified Features

- Sales Upload API
- Inventory APIs
- Sales Transaction APIs
- Invoice APIs
- Payment APIs
- Revenue Summary API
- Invoice Workflow
- Payment Workflow
- Revenue Calculations
- CSV Validation
- Filtering
- Pagination (Sales Transactions only)

---

# Conclusion

The backend implementation for **MarketMind AI – Milestone 2** has been successfully completed. All APIs have been developed, tested, and validated according to the **Software Requirements Specification (SRS)**. The backend is ready for frontend integration and final system testing with the **Security API Gateway** and **AI/ML modules**.
