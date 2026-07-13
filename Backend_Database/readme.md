# 📊 MarketMind AI – Backend

MarketMind AI is a Small Business Sales Intelligence Platform developed as part of the **Infosys Springboard Virtual Internship 7.0**.

This backend is built using **FastAPI**, **PostgreSQL**, and **SQLAlchemy**, providing ETL processing, inventory management, sales transaction management, and REST APIs.

---

# 🚀 Features

## ✅ ETL Pipeline

- Extract data from CSV files
- Data transformation and validation
- Column mapping
- Duplicate detection
- Missing value handling
- Automatic generation of:
  - Transaction IDs
  - Store IDs
  - Inventory table
  - Created By User IDs
- Load validated data into PostgreSQL

---

## ✅ Database

PostgreSQL relational database with the following tables:

- Roles
- Users
- Customers
- Stores
- Products
- Inventory
- Sales Transactions

---

## ✅ REST APIs

### Sales Upload

- Upload CSV
- Validate CSV schema
- Validate required columns

---

### Inventory CRUD

- Get All Inventory
- Get Inventory by Product ID
- Add Inventory
- Update Inventory
- Delete Inventory

---

### Sales Transaction CRUD

- Get All Sales
- Get Sale by Transaction ID
- Create Sale
- Update Sale
- Delete Sale

---

## ✅ Business Logic

- Automatic inventory stock decrement after every successful sale
- Inventory validation before sale creation
- Prevents sale if stock is insufficient

---

# 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| FastAPI | Backend Framework |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| Pandas | ETL Processing |
| Pydantic | Request Validation |
| Uvicorn | ASGI Server |
| Python | Programming Language |

---

# 📁 Project Structure

```
marketmind-backend/

│
├── app
│   ├── api
│   │   └── routes
│   │       ├── inventory.py
│   │       ├── sales.py
│   │       ├── sales_transaction.py
│   │       └── test_db.py
│   │
│   ├── core
│   │   ├── config.py
│   │   └── database.py
│   │
│   ├── etl
│   │   ├── transform.py
│   │   ├── load_data.py
│   │   ├── logs
│   │   ├── input
│   │   └── output
│   │
│   ├── models
│   │
│   ├── repositories
│   │   └── sales_transaction_repository.py
│   │
│   ├── schemas
│   │
│   └── main.py
│
├── requirements.txt
├── README.md
└── .env.example
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone <repository-url>
```

Move into the project

```bash
cd marketmind-backend
```

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

# ⚙️ Environment Variables

Create a `.env` file

Example

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/marketmind_ai
```

---

# ▶ Run the Application

```bash
uvicorn app.main:app --reload
```

---

# 📄 API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# 🗄 ETL Workflow

```
Raw CSV Dataset
        │
        ▼
Extract
        │
        ▼
Transform
        │
        ▼
Validation
        │
        ▼
Generate IDs
        │
        ▼
Load into PostgreSQL
```

---

# 🔄 Sales Workflow

```
Create Sale
      │
      ▼
Check Inventory
      │
      ▼
Enough Stock?
      │
 ┌────┴────┐
 │         │
Yes        No
 │         │
 ▼         ▼
Reduce     Return Error
Stock
 │
 ▼
Save Sale
```

---

# ✅ Completed Modules

- Database Schema
- SQLAlchemy Models
- CSV Upload API
- ETL Pipeline
- Inventory CRUD
- Sales Transaction CRUD
- Automatic Stock Management

---


# 👨‍💻 Developed For

**Infosys Springboard Virtual Internship 7.0**

Project:
**MarketMind AI – Small Business Sales Intelligence Platform**

Backend Stack:
- FastAPI
- PostgreSQL
- SQLAlchemy
- Python
