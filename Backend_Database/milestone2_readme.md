# 🚀 MarketMind AI Backend

Backend API for **MarketMind AI – Small Business Sales Intelligence Platform**, developed as part of the **Infosys Springboard Virtual Internship 7.0**.

The backend is built using **FastAPI**, **PostgreSQL**, and **SQLAlchemy**, providing REST APIs for inventory management, sales transactions, invoice generation, payment tracking, revenue analytics, and CSV data upload.

---

# 📌 Project Overview

MarketMind AI is an intelligent sales management platform that enables small businesses to:

- Manage inventory
- Record sales transactions
- Generate invoices
- Track payments
- Monitor revenue
- Upload sales datasets
- Support AI-based analytics and forecasting

---

# 🏗 Tech Stack

| Technology | Purpose |
|------------|---------|
| FastAPI | REST API Framework |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| Pydantic | Request & Response Validation |
| Pandas | CSV Processing |
| Uvicorn | ASGI Server |
| Docker | Containerization |
| Alembic | Database Migration |

---

# 📂 Project Structure

```
marketmind-backend/
│
├── alembic/
├── app/
│   ├── api/
│   │    └── routes/
│   ├── core/
│   ├── database/
│   ├── etl/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── main.py
│
├── uploads/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# 🗄 Database Modules

The backend contains the following database entities:

- Roles
- Users
- Customers
- Stores
- Products
- Inventory
- Sales Transactions
- Invoices
- Invoice Items
- Payments

---

# 🔗 Database Relationships

```
Roles
   │
Users
   │
   ├────────── Invoices
   │               │
   │               ├──────── Invoice Items
   │               ├──────── Payments
   │               └──────── Sales Transactions
   │
Customers ─────────┘

Stores
   ├──────── Invoices
   └──────── Sales Transactions

Products
   ├──────── Inventory
   ├──────── Invoice Items
   └──────── Sales Transactions
```

---

# 📦 API Modules

## Sales Upload

| Method | Endpoint |
|---------|----------|
| POST | /api/sales/upload |

Uploads and validates CSV sales data.

---

## Inventory APIs

| Method | Endpoint |
|---------|----------|
| GET | /inventory |
| GET | /inventory/{product_id} |
| POST | /inventory |
| PUT | /inventory/{product_id} |
| DELETE | /inventory/{product_id} |

Manages product inventory.

---

## Sales Transaction APIs

| Method | Endpoint |
|---------|----------|
| GET | /sales |
| GET | /sales/{transaction_id} |
| POST | /sales |
| PUT | /sales/{transaction_id} |
| DELETE | /sales/{transaction_id} |

Records sales and updates inventory automatically.

Pagination is implemented for GET All Sales.

---

## Invoice APIs

| Method | Endpoint |
|---------|----------|
| GET | /invoices |
| GET | /invoices/{invoice_id} |
| POST | /invoices |
| PUT | /invoices/{invoice_id} |
| DELETE | /invoices/{invoice_id} |

### Supported Filters

- payment_status
- customer_id
- invoice_number

Invoice creation automatically:

- validates customer
- validates product
- validates inventory
- generates invoice number
- calculates totals
- creates invoice items
- updates inventory

---

## Payment APIs

| Method | Endpoint |
|---------|----------|
| GET | /payments/{invoice_id} |
| POST | /payments |
| PUT | /payments/{payment_id} |
| DELETE | /payments/{payment_id} |

Supports:

- Full Payment
- Partial Payment
- Multiple Payments per Invoice

Automatically updates invoice payment status.

---

## Revenue Summary API

| Method | Endpoint |
|---------|----------|
| GET | /revenue/summary |

Returns:

- Total Revenue
- Outstanding Amount
- Daily Collections

---

# 📊 Business Features

✅ Inventory Management

✅ Sales Recording

✅ Invoice Generation

✅ Invoice Item Management

✅ Payment Tracking

✅ Revenue Dashboard

✅ CSV Upload & Validation

✅ Pagination

✅ Filtering

---

# 📈 Revenue Calculation

Revenue Summary includes:

- Total Revenue
- Outstanding Amount
- Daily Collections

Calculated directly from Invoice and Payment records.

---

# 🔒 Security

Current Development:

- Open APIs
- Swagger Testing
- Postman Testing

Final Integration:

- JWT Authentication
- RBAC
- API Gateway
- Audit Logging

(Handled by the Security Team.)

---

# 🧪 Testing

The backend has been tested using:

- Swagger UI
- Postman
- PostgreSQL

Verified Features:

- CRUD Operations
- Invoice Workflow
- Payment Workflow
- Revenue Summary
- CSV Validation
- Pagination
- Filtering

---

# 🐳 Running with Docker

Build:

```bash
docker-compose up --build
```

Application URLs:

Backend

```
http://localhost:8000
```

Swagger

```
http://localhost:8000/docs
```

PostgreSQL

```
localhost:5432
```

---

# 👨‍💻 Internship Milestones

## Milestone 1

- Database Design
- Schema Creation
- ETL
- CSV Upload
- Sales APIs
- Inventory APIs

---

## Milestone 2

- Invoice Module
- Invoice Items
- Payment Module
- Revenue Dashboard
- Advanced Filters
- Pagination
- Team Integration
- Docker Support

---

# 👥 Developed As Part Of

**Infosys Springboard Virtual Internship 7.0**

Project:

**MarketMind AI – Small Business Sales Intelligence Platform**

Backend Development & Database Engineering

---
