# MarketMind AI Backend

## Project Overview

MarketMind AI is an AI-powered retail analytics platform developed as part of the Infosys Springboard Virtual Internship.

The backend is built using **FastAPI**, **PostgreSQL**, and **SQLAlchemy ORM**. It provides REST APIs for uploading retail sales datasets, validating CSV files, storing data into a relational database, and supporting future AI-based sales analytics.

---

# Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.14 | Backend Development |
| FastAPI | REST API Framework |
| PostgreSQL | Relational Database |
| SQLAlchemy ORM | Database ORM |
| Alembic | Database Migration |
| Pandas | CSV Processing |
| Uvicorn | ASGI Server |
| python-dotenv | Environment Variable Management |
| python-multipart | File Upload Support |

---

# Project Structure

```
marketmind-backend/
│
├── alembic/
│
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── sales.py
│   │       └── test_db.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── role.py
│   │   ├── user.py
│   │   ├── customer.py
│   │   ├── product.py
│   │   ├── inventory.py
│   │   ├── store.py
│   │   ├── sales_transaction.py
│   │   └── __init__.py
│   │
│   ├── repositories/
│   │
│   ├── services/
│   │
│   ├── schemas/
│   │   ├── schema.sql
│   │   ├── seed_data.py
│   │   └── marketmind_sales_dataset.csv
│   │
│   ├── uploads/
│   │
│   └── main.py
│
├── requirements.txt
├── README.md
└── .env
```

---

# Features Implemented

## Day 1

### Project Initialization

- FastAPI project setup
- Virtual environment creation
- Dependency installation
- PostgreSQL integration
- Environment configuration using `.env`
- SQLAlchemy engine configuration
- Database session management

---

## Day 2

### Database Design

Implemented complete relational database schema using SQLAlchemy ORM.

### Tables Created

- Roles
- Users
- Customers
- Products
- Inventory
- Stores
- Sales Transactions

### Relationships Implemented

- Role → Users
- Customer → Sales Transactions
- Product → Inventory
- Product → Sales Transactions
- Store → Sales Transactions
- User → Sales Transactions

### Database Connectivity

- SQLAlchemy Engine configured
- SessionLocal configured
- PostgreSQL connection verified
- ORM queries tested successfully

---

## Day 3

### CSV Upload API

Implemented REST endpoint

```
POST /api/sales/upload
```

---

### File Upload

Implemented file upload using

- UploadFile
- File
- python-multipart

Supports only

```
CSV files
```

---

### CSV Schema Validation

Validated uploaded CSV against required columns.

Required columns

- invoice_id
- customer_id
- product_id
- quantity
- total_amount
- transaction_date

If validation fails

- Returns HTTP 400
- Displays missing column names

If validation succeeds

Returns

- filename
- total rows
- total columns
- detected column names

---

### Error Handling

Implemented

- Invalid file type detection
- Missing column validation
- HTTPException responses

---

# API Endpoints

## Test Database Connection

```
GET /test-db
```

Purpose

- Verify PostgreSQL connectivity
- Verify SQLAlchemy ORM connectivity
- Count records from SalesTransaction table

---

## Upload Sales CSV

```
POST /api/sales/upload
```

Purpose

- Upload CSV dataset
- Validate schema
- Return dataset metadata

---

# Current Status

Completed

- FastAPI setup
- PostgreSQL integration
- SQLAlchemy ORM
- Database Models
- Relationships
- Database Testing
- CSV Upload API
- CSV Schema Validation

---

# Upcoming Development

The following features are planned in the next development phase:

- Data Cleaning Pipeline
- Duplicate Removal
- Missing Value Handling
- Data Validation
- ETL Pipeline
- Bulk Database Loading
- Repository Layer
- Service Layer
- Analytics APIs
- Dashboard APIs
- AI Prediction Integration

---

# Installation

Create virtual environment

```bash
python -m venv .venv
```

Activate virtual environment

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Configure Environment

Create `.env`

```
DATABASE_URL=postgresql://username:password@localhost:5432/marketmind_ai
```

---

# Run Application

```bash
python -m uvicorn app.main:app --reload
```

---

# API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# Database

Database

```
PostgreSQL
```

ORM

```
SQLAlchemy
```

Migration Tool

```
Alembic
```

---

# Author

**Palak Ganwani**

Backend Development Team

Infosys Springboard Virtual Internship 7.0

MarketMind AI Project
