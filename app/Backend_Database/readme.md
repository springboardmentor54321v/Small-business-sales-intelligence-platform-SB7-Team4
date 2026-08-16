# MarketMind AI — Backend & Database Domain

**MarketMind AI – Small Business Sales Intelligence Platform**

Backend & Database Domain  
Infosys Springboard Virtual Internship 7.0

---

## 1. Project Overview

MarketMind AI is a small-business sales intelligence platform designed to help businesses manage sales, customers, products, inventory and invoices while providing a foundation for AI-powered business analytics.

The Backend & Database domain is responsible for the **data and business-logic backbone of the platform**.

The backend provides REST APIs for:

- Sales data ingestion
- Sales transaction management
- Customer management
- Inventory management
- Invoice management
- Invoice item management
- Payment management
- Revenue summaries
- Low-stock notifications
- Overdue-invoice notifications
- Database persistence and relational integrity
- Data validation and transformation
- Pagination, filtering and search
- Bulk update operations
- Automated backend testing
- Integration with the Frontend, Security/API Gateway, AI/ML and DevOps domains

The backend was developed incrementally across **four milestones**, with each milestone extending the functionality created in the previous one.

---

# 2. Backend & Database Domain Responsibility

The Backend & Database domain owned the:

- Data Ingestion Layer
- Storage Layer
- PostgreSQL database
- SQLAlchemy ORM models
- Database relationships
- CSV upload and validation
- ETL and data-cleaning pipeline
- Sales transaction APIs
- Inventory APIs
- Customer APIs
- Invoice APIs
- Invoice item persistence
- Payment APIs
- Revenue summary APIs
- Notification APIs
- Repository layer
- Service layer
- Pydantic request/response schemas
- Database business rules
- Inventory-stock synchronization
- Invoice-payment synchronization
- Automated backend tests
- Final backend integration and hardening


---

# 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | REST API framework |
| PostgreSQL | Relational database |
| SQLAlchemy | ORM and database interaction |
| Pydantic | Request/response validation |
| Pandas | CSV processing and ETL |
| psycopg2 | PostgreSQL database driver |
| Uvicorn | ASGI application server |
| Alembic | Database migration support |
| python-dotenv | Environment configuration |
| python-multipart | Multipart file upload support |
| pytest | Automated backend testing |
| Git & GitHub | Version control |

---

# 4. Backend Architecture

The backend follows a layered architecture:

```text
Frontend / API Gateway
        |
        v
FastAPI Routes
        |
        v
Pydantic Schemas
        |
        v
Service Layer
        |
        v
Repository Layer
        |
        v
SQLAlchemy ORM Models
        |
        v
PostgreSQL Database
```

For CSV ingestion, the flow is:

```text
CSV File
   |
   v
Upload API
   |
   v
Pandas DataFrame
   |
   v
Column Detection & Mapping
   |
   v
Validation / Cleaning
   |
   v
Store Resolution
   |
   v
Bulk Import Logic
   |
   v
Invoices + Invoice Items + Sales Transactions
   |
   v
PostgreSQL
```

---

# 5. Final Backend Project Structure

```text
marketmind-backend/
│
├── app/
│   │
│   ├── api/
│   │   └── routes/
│   │       ├── customer.py
│   │       ├── inventory.py
│   │       ├── invoice.py
│   │       ├── notification.py
│   │       ├── payment.py
│   │       ├── revenue.py
│   │       ├── sales.py
│   │       └── sales_transaction.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   │
│   ├── database/
│   │   ├── schema.sql
│   │   ├── Milestone2_schema.sql
│   │   ├── seed_data_milestone2.sql
│   │   ├── MarketMind_ER.pdf
│   │   └── Milestone2_ER_Diagram.jpg
│   │
│   ├── etl/
│   │   ├── input/
│   │   │   └── cleaned_dataset.csv
│   │   ├── output/
│   │   │   ├── customers.csv
│   │   │   ├── inventory.csv
│   │   │   ├── products.csv
│   │   │   ├── sales_transactions.csv
│   │   │   ├── stores.csv
│   │   │   └── validated_dataset.csv
│   │   ├── logs/
│   │   │   └── etl.log
│   │   ├── transform.py
│   │   └── load_data.py
│   │
│   ├── models/
│   │   ├── role.py
│   │   ├── user.py
│   │   ├── customer.py
│   │   ├── store.py
│   │   ├── product.py
│   │   ├── inventory.py
│   │   ├── sales_transaction.py
│   │   ├── invoice.py
│   │   ├── invoice_item.py
│   │   └── payment.py
│   │
│   ├── repositories/
│   │   ├── customer_repository.py
│   │   ├── invoice_repository.py
│   │   ├── invoice_item_repository.py
│   │   ├── notification_repository.py
│   │   ├── payment_repository.py
│   │   ├── revenue_repository.py
│   │   └── sales_transaction_repository.py
│   │
│   ├── schemas/
│   │   ├── customer.py
│   │   ├── inventory.py
│   │   ├── invoice.py
│   │   ├── invoice_item.py
│   │   ├── notification.py
│   │   ├── payment.py
│   │   ├── product.py
│   │   ├── revenue.py
│   │   ├── sales_transaction.py
│   │   ├── sales_upload.py
│   │   └── store.py
│   │
│   ├── services/
│   │   ├── invoice_service.py
│   │   ├── notification_service.py
│   │   ├── payment_service.py
│   │   ├── revenue_service.py
│   │   └── sales_service.py
│   │
│   ├── utils/
│   │   └── sales_csv.py
│   │
│   └── main.py
│
├── tests/
│   ├── test_customer.py
│   ├── test_integration.py
│   ├── test_inventory.py
│   ├── test_invoice.py
│   ├── test_notification.py
│   ├── test_payment.py
│   ├── test_revenue.py
│   ├── test_sales_transaction.py
│   └── test_sales_upload.py
│
├── alembic/
├── requirements.txt
├── .env.example
└── README.md
```

---

# 6. Database Design

## 6.1 Core Tables

The final database contains the foundational entities:

1. `roles`
2. `users`
3. `customers`
4. `stores`
5. `products`
6. `inventory`
7. `sales_transactions`

Milestone 2 extends the database with:

8. `invoices`
9. `invoice_items`
10. `payments`

---

# 7. Database Relationships

The main relationships are:

```text
Roles
  |
  └── Users
        |
        ├── Sales Transactions
        └── Invoices

Customers
  |
  ├── Sales Transactions
  └── Invoices

Stores
  |
  ├── Sales Transactions
  └── Invoices

Products
  |
  ├── Inventory
  ├── Sales Transactions
  └── Invoice Items

Invoices
  |
  ├── Invoice Items
  ├── Payments
  └── Sales Transactions
```

Important relationships include:

- One role can be assigned to multiple users.
- One customer can have multiple sales transactions.
- One customer can have multiple invoices.
- One product has an associated inventory record.
- One product can appear in multiple sales transactions.
- One product can appear in multiple invoice items.
- One invoice can contain multiple invoice items.
- One invoice can have multiple payment records.
- Sales transactions can be associated with invoices.
- Stores are associated with sales transactions and invoices.

---

# 8. Database Entities

## Roles

Stores application roles.

Main fields:

- `id`
- `name`
- `created_at`

---

## Users

Stores system users and their role association.

Main fields:

- `id`
- `name`
- `email`
- `password_hash`
- `role_id`
- `created_at`

Authentication and RBAC functionality belongs to the Security/API Gateway domain, while the Backend domain maintains the user/role database structure.

---

## Customers

Stores customer information.

Main fields:

- `id`
- `customer_id`
- `name`
- `email`
- `phone`
- `created_at`

Customer APIs support:

- Listing customers
- Pagination
- Search
- Creating customers
- Deleting customers

---

## Stores

Stores business/store information.

Main fields:

- `id`
- `store_id`
- `store_name`
- `location`
- `created_at`

Store information is also used during CSV ingestion to resolve sales records to the correct store.

---

## Products

Stores product master information.

Main fields:

- `id`
- `product_id`
- `product_name`
- `category`
- `unit_price`
- `created_at`

Product information acts as the authoritative source for product pricing and product metadata.

---

## Inventory

Stores current product stock.

Main fields:

- `id`
- `product_id`
- `stock_quantity`
- `low_stock_threshold`
- `updated_at`

Inventory is directly connected to sales and invoice creation.

When a valid sale is recorded:

```text
Sale Quantity
      |
      v
Inventory Stock
      |
      v
Stock Decrement
```

The backend also prevents a sale/invoice from being created when sufficient stock is not available.

---

## Sales Transactions

Stores individual sales transaction records.

Main fields include:

- `id`
- `transaction_id`
- `invoice_id`
- `transaction_date`
- `customer_id`
- `product_id`
- `store_id`
- `quantity`
- `unit_price`
- `discount`
- `total_amount`
- `payment_method`
- `created_by_user_id`
- `created_at`

The backend calculates the authoritative unit price from the Product table instead of trusting a client-provided price.

---

# 9. Milestone 1 — Foundation, Sales Data & Inventory

## Milestone Objective

Milestone 1 established the foundational database and backend layer of MarketMind AI.

The SRS assigned the Backend & Database Engineer ownership of the Data Ingestion Layer and Storage/Database Layer.

---

## 9.1 Database Foundation

The first milestone created the core database structure for:

- Roles
- Users
- Customers
- Products
- Stores
- Inventory
- Sales Transactions

The ER design was created and the PostgreSQL environment was established.

SQLAlchemy ORM models were created for database interaction.

---

## 9.2 Database Implementation

The database schema was implemented using SQLAlchemy and PostgreSQL.

The database included:

- Primary keys
- Unique identifiers
- Foreign keys
- Relationships
- Numeric financial fields
- Timestamps
- Inventory constraints
- Referential integrity

Seed/sample data was also prepared for development and integration testing.

---

## 9.3 ETL & Data Preparation

A complete ETL pipeline was developed to prepare the sales dataset before database loading.

The pipeline performs tasks such as:

- Reading the cleaned dataset
- Standardizing columns
- Mapping source columns
- Creating customer identifiers
- Creating product information
- Creating store information
- Generating inventory records
- Assigning store IDs
- Assigning `created_by_user_id`
- Validating required columns
- Removing invalid rows
- Generating database-ready CSV files
- Logging ETL operations

The final packaged validated dataset contains **51,290 validated sales records**.

Generated datasets include:

```text
customers.csv
products.csv
stores.csv
inventory.csv
sales_transactions.csv
validated_dataset.csv
```

---

# 10. Milestone 1 — Sales CSV Upload API

The main ingestion endpoint was:

```http
POST /api/sales/upload
```

The API accepts a CSV file through multipart form-data.

---

## Upload Processing Flow

```text
CSV Upload
   |
   v
File Type Validation
   |
   v
CSV Parsing using Pandas
   |
   v
Column Detection & Mapping
   |
   v
Required Field Validation
   |
   v
Store Resolution
   |
   v
Duplicate / Existing Record Handling
   |
   v
Invoice & Invoice Item Creation
   |
   v
Sales Transaction Storage
   |
   v
Inventory Synchronization
```

The final implementation supports:

- CSV file validation
- CSV parsing
- Known column aliases
- Column normalization
- Store resolution using location information
- Validation of uploaded records
- Bulk sales import
- Duplicate/previous-record handling
- Automatic invoice creation during bulk import
- Invoice-item creation
- Sales transaction persistence

---

# 11. Milestone 1 — Inventory APIs

The Inventory module provides CRUD operations.

Implemented functionality:

- View inventory
- View inventory by product
- Add inventory
- Update inventory
- Delete inventory
- Search inventory
- Filter inventory by category
- Paginate inventory
- Bulk update inventory
- Low-stock threshold management

Inventory is connected to product information so responses can include:

- Product ID
- Product name
- Category
- Stock quantity
- Low-stock threshold

---

# 12. Milestone 1 — Sales Transaction APIs

The final backend supports complete sales transaction CRUD operations.

Implemented functionality:

- Get all sales
- Get sale by transaction ID
- Create sale
- Update sale
- Delete sale
- Pagination
- Date-range filtering
- Search

The sales API also contains business logic for:

- Product validation
- Inventory validation
- Stock availability checking
- Authoritative product pricing
- Discount calculation
- Total calculation
- Automatic inventory decrement
- Inventory restoration when transaction quantity is reduced

---

# 13. Milestone 1 Integration

The Backend domain was integrated with:

- Frontend
- Security/API Gateway
- AI/ML
- DevOps/Integration

The backend provided documented APIs and database structures required by the other domains.

The SRS acceptance criteria required that uploaded sales data reach PostgreSQL and that recording a sale correctly reduce inventory.

---

# 14. Milestone 2 — Invoice & Payment Management

## Milestone Objective

Milestone 2 expanded the backend from basic sales/inventory functionality into a more complete business transaction system.

The main Backend & Database focus became:

- Invoice management
- Invoice items
- Payments
- Payment status
- Overdue invoice logic
- Revenue summaries
- Expanded sales/inventory APIs

The SRS specifically assigned the Backend domain responsibility for full invoice management, payments, reminders and revenue summaries.

---

# 15. Milestone 2 — Invoice Database Design

Three new tables were introduced:

```text
invoices
invoice_items
payments
```

---

## Invoices

Main fields:

- `invoice_id`
- `invoice_number`
- `customer_id`
- `store_id`
- `created_by_user_id`
- `invoice_date`
- `due_date`
- `subtotal`
- `discount_amount`
- `tax_amount`
- `total_amount`
- `payment_status`
- `invoice_status`
- `notes`
- `created_at`
- `updated_at`

---

## Invoice Items

Each invoice can contain multiple products.

Main fields:

- `invoice_item_id`
- `invoice_id`
- `product_id`
- `quantity`
- `unit_price`
- `discount`
- `tax`
- `line_total`
- `category_snapshot`
- `product_name_snapshot`
- `created_at`

Product and category snapshots preserve the product information associated with the invoice item.

---

## Payments

Main fields:

- `payment_id`
- `invoice_id`
- `payment_date`
- `amount_paid`
- `payment_method`
- `transaction_reference`
- `remarks`
- `created_at`

An invoice can therefore have multiple payment records.

---

# 16. Milestone 2 — Create Invoice Workflow

The invoice creation service performs multiple validations before creating the invoice.

```text
Create Invoice Request
        |
        v
Validate Customer
        |
        v
Validate Store
        |
        v
Validate Products
        |
        v
Check Inventory
        |
        v
Calculate Subtotal
        |
        v
Calculate Discount
        |
        v
Calculate Tax
        |
        v
Calculate Total
        |
        v
Generate Invoice Number
        |
        v
Create Invoice
        |
        v
Create Invoice Items
        |
        v
Reduce Inventory
        |
        v
Commit Transaction
```

The backend automatically generates invoice numbers beginning from the configured invoice sequence.

Example:

```text
INV900001
INV900002
INV900003
...
```

---

# 17. Invoice Business Rules

The backend applies the following rules:

### Customer Validation

An invoice cannot be created for a non-existing customer.

### Store Validation

An invoice must reference an existing store.

### Product Validation

Every invoice item must reference an existing product.

### Inventory Validation

The requested quantity cannot exceed available inventory.

### Price Authority

The product's stored unit price is used when calculating invoice totals.

### Inventory Synchronization

Creating an invoice reduces the corresponding inventory quantity.

### Invoice Status

Invoices maintain both:

- Payment status
- Invoice status

Examples include:

```text
Payment Status:
Pending
Partially Paid
Paid
```

and:

```text
Invoice Status:
Generated
Completed
```

---

# 18. Milestone 2 — Invoice APIs

Implemented endpoints include:

```http
GET    /invoices/
GET    /invoices/{invoice_id}
POST   /invoices/
PUT    /invoices/{invoice_id}
DELETE /invoices/{invoice_id}
PUT    /invoices/bulk-update
```

The invoice list supports:

- Pagination
- Payment-status filtering
- Invoice-status filtering
- Customer filtering
- Invoice-number search

---

# 19. Milestone 2 — Payment Management

Payment processing was implemented as a service rather than simply inserting a payment record.

The workflow is:

```text
Payment Request
      |
      v
Validate Invoice
      |
      v
Create Payment
      |
      v
Calculate Total Paid
      |
      v
Update Invoice Payment Status
      |
      v
Check Overdue Condition
      |
      v
Return Payment Summary
```

Payment status is determined using the total amount paid.

```text
Total Paid = 0
      → Pending

0 < Total Paid < Invoice Total
      → Partially Paid

Total Paid >= Invoice Total
      → Paid
```

The payment response also provides:

- Invoice status
- Invoice total
- Total amount paid
- Remaining amount
- Overdue reminder status

---

# 20. Milestone 2 — Payment APIs

Implemented endpoints:

```http
GET    /payments/
GET    /payments/{payment_id}
POST   /payments/
PUT    /payments/{payment_id}
DELETE /payments/{payment_id}
```

---

# 21. Milestone 2 — Revenue Summary

A Revenue Summary API was implemented for dashboard consumption.

Endpoint:

```http
GET /revenue/summary
```

The response provides:

```text
total_revenue
total_outstanding
daily_collections
```

### Total Revenue

Calculated from recorded payment amounts.

### Total Outstanding

Calculated from invoices whose payment status is not `Paid`.

### Daily Collections

Calculated from payments received on the current date.

The SRS specifically required these values for Business Owner dashboard reporting.

---

# 22. Milestone 2 — Integration

The backend invoice, payment and revenue functionality was integrated with:

- Frontend Invoice screen
- Business Owner dashboard
- Security/RBAC layer
- Database/DevOps environment
- AI/ML data consumers

The Milestone 2 acceptance criteria required successful invoice creation, payment updates, overdue detection and accurate revenue/outstanding summaries.

---

# 23. Milestone 3 — Notifications, Advanced API Operations & Testing

## Milestone Objective

Milestone 3 focused on making the existing backend **smarter, more scalable and more reliable** without introducing a new dataset.

The Backend & Database domain was responsible for:

- Low-stock notifications
- Overdue-invoice notifications
- Pagination
- Filtering
- Search
- Bulk updates
- Automated backend tests
- Integration testing
- Backend hardening

The SRS explicitly required these capabilities while continuing to use the existing dataset.

---

# 24. Milestone 3 — Notification System

A unified Notifications API was introduced:

```http
GET /notifications
```

The API combines two notification categories.

---

## Low-Stock Notifications

The backend checks:

```text
stock_quantity <= low_stock_threshold
```

Products satisfying this condition generate low-stock notifications.

Severity is calculated based on how far stock has fallen below the threshold.

Levels include:

```text
CRITICAL
HIGH
MEDIUM
```

---

## Overdue Invoice Notifications

An invoice is considered overdue when:

```text
due_date < current_date
AND
payment_status != Paid
```

The backend specifically considers:

```text
Pending
Partially Paid
```

invoices for overdue notification generation.

Severity is determined using the number of overdue days.

---

# 25. Notification Response

Notifications contain information such as:

- Notification type
- Severity
- Title
- Message
- Reference ID

Notification types include:

```text
LOW_STOCK
OVERDUE_INVOICE
```

This allows the Frontend to display a single notification panel instead of separately querying multiple backend resources.

---

# 26. Milestone 3 — Pagination

Pagination was added to major list APIs.

The general pattern is:

```text
page
page_size
```

The backend uses database offset/limit operations to retrieve only the requested records.

Pagination was added to:

- Sales
- Inventory
- Invoices
- Customers

This prevents the backend from unnecessarily returning the entire dataset for every request.

---

# 27. Milestone 3 — Filtering & Search

### Sales

Supported filters/search:

- Start date
- End date
- Transaction ID
- Invoice ID
- Customer ID
- Product ID

### Inventory

Supported filters/search:

- Category
- Product ID
- Product name

### Invoices

Supported filters/search:

- Payment status
- Invoice status
- Customer ID
- Invoice number

### Customers

Supported:

- Customer search

---

# 28. Milestone 3 — Bulk Updates

Bulk operations were introduced for large-scale updates.

### Bulk Inventory Update

```http
PUT /inventory/bulk-update
```

Allows multiple inventory records to be updated in a single request.

### Bulk Invoice Update

```http
PUT /invoices/bulk-update
```

Allows multiple invoices to have their payment status updated together.

Validation handles:

- Empty update requests
- Invalid IDs
- Missing records
- Database rollback on failure

The SRS specifically required bulk invoice and inventory operations with edge-case handling.

---

# 29. Milestone 3 — Automated Backend Testing

Automated tests were added using `pytest`.

The final backend contains test modules for:

```text
test_customer.py
test_integration.py
test_inventory.py
test_invoice.py
test_notification.py
test_payment.py
test_revenue.py
test_sales_transaction.py
test_sales_upload.py
```

The suite contains tests covering:

- Customer operations
- Inventory operations
- Invoice creation and logic
- Payment processing
- Revenue calculations
- Notifications
- Sales transactions
- CSV upload
- Integration workflows

The backend test suite contains **31 individual test functions across 9 test modules** in the final project archive.

---

# 30. Milestone 3 — Integration Testing

An integration test was added for the core business workflow:

```text
Sales
  |
  v
Inventory
  |
  v
Invoice
  |
  v
Notification
```

This validates that the backend modules work together instead of only testing them independently.

The SRS explicitly required automated testing of the Sales → Inventory → Invoice → Notification chain.

---

# 31. Milestone 4 — Final Backend Testing & Deployment Readiness

## Milestone Objective

Milestone 4 was the final milestone.

Unlike Milestone 3, which intentionally remained local, Milestone 4 focused on:

- Final testing
- Error hardening
- Backend deployment
- Live API verification
- Frontend/backend integration
- Security verification
- Load testing
- Final documentation
- Demo readiness

The SRS required all backend APIs from Milestones 1–3 to remain functional on the final deployment without replacing the existing dataset.

---

# 32. Milestone 4 — Backend Finalization

The final backend work included reviewing the complete API inventory:

```text
Sales
Inventory
Customers
Invoices
Payments
Revenue
Notifications
```

The backend was hardened against:

- Invalid input
- Missing data
- Invalid IDs
- Insufficient inventory
- Missing database records
- Invalid CSV uploads
- Unexpected database operations

Error responses were standardized using FastAPI HTTP exceptions where appropriate.

---

# 33. Milestone 4 — Environment Configuration

Configuration values are maintained through environment variables rather than hard-coded application values.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/marketmind_ai
```

Sensitive credentials should never be committed to GitHub.

The repository contains:

```text
.env.example
```

for documenting required configuration variables.

---

# 34. Milestone 4 — Deployment Integration

The backend was prepared for integration with the project's deployment infrastructure.

The Backend domain worked with the DevOps/Integration domain to ensure:

- Database connectivity
- Backend configuration
- API availability
- Frontend-to-backend communication
- Environment-specific configuration
- Live API verification
- Deployment-specific issue resolution

The final milestone's SRS specifically called for testing Sales, Inventory, Invoice, Notifications and Revenue APIs against the live environment.

---

# 35. Final API Catalog

The final backend exposes the following major API groups.

## Sales Upload

```http
POST /api/sales/upload
```

Uploads and processes a sales CSV.

---

## Sales Transactions

```http
GET    /sales/
GET    /sales/{transaction_id}
POST   /sales/
PUT    /sales/{transaction_id}
DELETE /sales/{transaction_id}
```

---

## Customers

```http
GET    /customers/
POST   /customers/
DELETE /customers/{customer_id}
```

---

## Inventory

```http
GET    /inventory/
GET    /inventory/{product_id}
POST   /inventory/
PUT    /inventory/{product_id}
DELETE /inventory/{product_id}
PUT    /inventory/bulk-update
```

---

## Invoices

```http
GET    /invoices/
GET    /invoices/{invoice_id}
POST   /invoices/
PUT    /invoices/{invoice_id}
DELETE /invoices/{invoice_id}
PUT    /invoices/bulk-update
```

---

## Payments

```http
GET    /payments/
GET    /payments/{payment_id}
POST   /payments/
PUT    /payments/{payment_id}
DELETE /payments/{payment_id}
```

---

## Revenue

```http
GET /revenue/summary
```

---

## Notifications

```http
GET /notifications
```

---

# 36. API Count

The final backend implementation contains **26 registered API operations** across the major Backend & Database modules.

These cover:

- Sales ingestion
- Sales CRUD
- Customer management
- Inventory management
- Invoice management
- Payment management
- Revenue reporting
- Notifications
- Bulk operations
- Search/filter/pagination functionality

---

# 37. Repository Layer

The repository layer isolates database queries from the API routes.

Implemented repositories include:

```text
customer_repository.py
invoice_repository.py
invoice_item_repository.py
notification_repository.py
payment_repository.py
revenue_repository.py
sales_transaction_repository.py
```

Responsibilities include:

- Database queries
- Record creation
- Record retrieval
- Updates
- Deletes
- Filtering
- Pagination
- Bulk operations
- Database aggregation

This keeps database-specific logic separate from API routing.

---

# 38. Service Layer

The service layer contains business logic that is more complex than simple CRUD.

Implemented services include:

```text
invoice_service.py
notification_service.py
payment_service.py
revenue_service.py
sales_service.py
```

Examples of service-level business rules:

- Invoice number generation
- Invoice total calculation
- Product validation
- Customer validation
- Store validation
- Inventory validation
- Payment status calculation
- Overdue invoice detection
- Notification severity calculation
- Revenue calculation
- Bulk invoice processing

---

# 39. Pydantic Schema Layer

Pydantic schemas are used to validate API input and structure API output.

Schemas are implemented for:

- Customers
- Inventory
- Invoices
- Invoice items
- Payments
- Revenue
- Sales transactions
- Notifications
- Product/store data

Examples of validation include:

- Required fields
- Data types
- Customer ID validation
- Customer name validation
- Email format validation
- Optional fields
- Request/response serialization

---

# 40. Data Integrity & Business Rules

The backend maintains several important integrity rules.

### Product Integrity

Products must exist before related inventory, sales or invoice-item records are created.

### Customer Integrity

Sales and invoices must reference valid customers.

### Store Integrity

Sales and invoices must reference valid stores.

### Inventory Integrity

Stock cannot become negative through valid sale/invoice operations.

### Invoice Integrity

Invoice items must reference valid invoices and products.

### Payment Integrity

Payments must reference an existing invoice.

### Payment Status Integrity

Invoice payment status is recalculated based on total payments.

### Financial Integrity

Invoice and sales totals are calculated using database/product values rather than relying solely on client-provided calculations.

---

# 41. CSV Column Processing

The backend includes a CSV utility:

```text
app/utils/sales_csv.py
```

It supports detection and mapping of known column aliases.

This allows the backend to work with standardized and known variants of sales CSV files rather than requiring every input file to have exactly the same original column names.

The ingestion process ultimately standardizes the data into the backend's expected structure.

---

# 42. ETL Pipeline

The ETL implementation is located under:

```text
app/etl/
```

### Transformation

```text
transform.py
```

Responsible for:

- Reading source data
- Standardizing fields
- Creating identifiers
- Preparing customer records
- Preparing product records
- Preparing store records
- Preparing inventory records
- Preparing sales transaction records
- Validating required fields
- Generating output datasets

### Loading

```text
load_data.py
```

Responsible for loading generated datasets into PostgreSQL through SQLAlchemy sessions.

---

# 43. Generated Database Datasets

The final backend archive contains generated datasets for:

```text
Customers
Products
Stores
Inventory
Sales Transactions
Validated Dataset
```

The packaged validated dataset contains:

```text
51,290 sales records
```

and the generated sales transaction CSV contains the standardized database-ready sales structure.

---

# 44. Seed Data

Milestone 2 seed data was also created for invoice/payment testing.

The seed file:

```text
app/database/seed_data_milestone2.sql
```

contains sample records for:

- Invoices
- Invoice items
- Payments

Example invoice sequence:

```text
INV900001
INV900002
...
INV900010
```

The seed data provides different payment states such as:

```text
Paid
Pending
Partially Paid
```

which makes it possible to test invoice, payment, revenue and notification logic.

---

# 45. API Documentation

FastAPI automatically provides interactive API documentation.

After starting the backend:

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

Swagger can be used to:

- View all API endpoints
- Inspect request schemas
- Inspect response schemas
- Test APIs
- Upload CSV files
- Test query parameters
- Review HTTP responses

---

# 46. Running the Backend

## 46.1 Create Virtual Environment

Windows:

```bash
python -m venv .venv
```

Activate:

```bash
.venv\Scripts\activate
```

---

## 46.2 Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 46.3 Configure Environment

Create a `.env` file.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/MarketMind_AI
```

Use the actual PostgreSQL credentials configured for the local environment.

---

## 46.4 Start PostgreSQL

Ensure the PostgreSQL service is running and the MarketMind AI database exists.

---

## 46.5 Start FastAPI

Run:

```bash
python -m uvicorn app.main:app --reload
```

The backend will normally be available at:

```text
http://127.0.0.1:8000
```

---

# 47. Running Tests

The project uses pytest.

Run:

```bash
pytest
```

For more detailed output:

```bash
pytest -v
```

The test suite covers:

```text
Customer
Inventory
Invoice
Payment
Revenue
Notifications
Sales Transactions
Sales Upload
Integration
```

---

# 48. Main Backend Data Flow

The final backend can be understood through the following business flow:

```text
                CSV / Manual Sale
                       |
                       v
                Sales API
                       |
                       v
              Sales Transaction
                       |
              +--------+--------+
              |                 |
              v                 v
         Inventory          Invoice
          Update           Generation
                                |
                         +------+------+
                         |             |
                         v             v
                  Invoice Items     Payments
                                        |
                                        v
                               Payment Status
                                        |
                         +--------------+--------------+
                         |                             |
                         v                             v
                  Revenue Summary              Notifications
```

---

# 49. Example Business Scenario

A Sales Executive records a sale.

### Step 1 — Product Validation

The backend checks whether the product exists.

### Step 2 — Inventory Validation

The backend checks whether sufficient stock is available.

### Step 3 — Price Retrieval

The current product price is retrieved from the database.

### Step 4 — Amount Calculation

The backend calculates:

```text
Subtotal
Discount
Tax
Final Total
```

### Step 5 — Invoice Creation

An invoice is generated and assigned an invoice number.

### Step 6 — Invoice Items

Each purchased product is stored as an invoice item.

### Step 7 — Inventory Update

The sold quantity is deducted from inventory.

### Step 8 — Payment

A payment can later be recorded against the invoice.

### Step 9 — Invoice Status

The payment service updates:

```text
Pending
Partially Paid
Paid
```

### Step 10 — Notifications

If the invoice becomes overdue or stock falls below the threshold, the notification system exposes an alert.

### Step 11 — Revenue

The Revenue Summary API reflects payment collections and outstanding amounts.

---

# 50. Backend Integration With Other Domains

## Frontend

The Backend provides data for:

- Sales dashboard
- Inventory dashboard
- Customer information
- Invoice screens
- Revenue summary
- Notifications

---

## Security/API Gateway

The Security domain handles:

- JWT authentication
- RBAC
- Gateway security
- Request authorization
- Rate limiting
- Audit functionality

The backend provides the routes and database resources that those security controls protect.

---

## AI/ML

The Backend provides structured business data required by AI/ML services, including:

- Customer information
- Product information
- Sales history
- Transaction quantities
- Prices
- Discounts
- Revenue-related data
- Inventory information

The AI/ML domain owns the actual forecasting and predictive models.

---

## DevOps/Integration

The Backend works with the DevOps domain for:

- Local integrated execution
- Docker-based integration
- CI testing
- Environment configuration
- Database connectivity
- Deployment
- Final live verification

---

# 51. Security Boundary

The backend is designed to work behind the separate **Security API Gateway**.

The intended architecture is:

```text
Frontend
    ↓
Security API Gateway
    ↓
FastAPI Backend
    ↓
PostgreSQL
```

The Security Gateway is maintained separately from the backend application and integrated at the Docker/deployment level..

---

# 52. Docker and Deployment

The backend is containerized using Docker.

The backend Docker container runs FastAPI on:

```text
0.0.0.0:8000
```

The Docker Compose architecture contains services for:

```text
PostgreSQL
FastAPI Backend
Security API Gateway
AI/ML Service
Notifications Service
Frontend
```

Within the Docker network, services communicate using Docker service names.

Examples:

```text
Gateway → backend:8000
Backend → db:5432
Gateway → aiml:5000
Gateway → notifications:5003
```

Deployment-specific details, including the final deployment platform, live URLs, environment configuration, and final deployment results, should be added after deployment is completed.

---

# 53. Milestone-Wise Summary

| Milestone | Backend & Database Contribution |
|---|---|
| Milestone 1 | PostgreSQL foundation, SQLAlchemy models, ER design, ETL, CSV upload, sales transactions, inventory CRUD and stock synchronization |
| Milestone 2 | Invoice management, invoice items, payments, payment status, overdue logic, revenue summary and expanded sales/inventory functionality |
| Milestone 3 | Low-stock notifications, overdue-invoice notifications, pagination, filtering, search, bulk updates, automated tests and integration testing |
| Milestone 4 | Final API review, error hardening, deployment preparation, live API verification, load testing support, final integration and documentation |

---

# 54. Final Backend Deliverables

The completed Backend & Database domain contains:

- PostgreSQL database design
- SQLAlchemy ORM models
- Database relationships
- SQL schema files
- ER diagrams
- ETL transformation pipeline
- ETL loading pipeline
- Cleaned and validated datasets
- Sales CSV upload API
- Sales transaction CRUD APIs
- Customer APIs
- Inventory CRUD APIs
- Inventory bulk update API
- Invoice APIs
- Invoice item persistence
- Invoice bulk update API
- Payment APIs
- Revenue summary API
- Notification API
- Low-stock detection
- Overdue invoice detection
- Pagination
- Filtering
- Search
- Business validation
- Inventory synchronization
- Payment status synchronization
- Repository layer
- Service layer
- Pydantic schema layer
- Automated backend tests
- Integration tests
- API documentation
- Final backend integration and deployment support

---

# 55. Final Project Outcome

Across the four milestones, the Backend & Database domain evolved from a basic PostgreSQL-backed sales upload module into a complete business transaction and data-management backend.

The progression was:

```text
Milestone 1
Foundation
    |
    v
Database + Sales + Inventory
    |
    v
Milestone 2
Invoice + Payment + Revenue
    |
    v
Milestone 3
Notifications + Pagination + Filtering
+ Bulk Operations + Automated Testing
    |
    v
Milestone 4
Hardening + Final Integration
+ Deployment Verification + Documentation
```

The final backend provides the **data foundation and business transaction layer** required by the rest of MarketMind AI.

It connects raw sales data to structured PostgreSQL storage, inventory management, invoices, payments, revenue calculations and operational notifications while exposing REST APIs that can be consumed by the Frontend, Security/API Gateway and AI/ML domains.

---

# 56. Project Information

**Project:** MarketMind AI – Small Business Sales Intelligence Platform

**Internship:** Infosys Springboard Virtual Internship 7.0

**Domain:** Backend & Database

**Primary Technologies:**

```text
Python
FastAPI
PostgreSQL
SQLAlchemy
Pydantic
Pandas
pytest
Uvicorn
Alembic
```

**Backend Entry Point:**

```text
app/main.py
```

**Database:**

```text
PostgreSQL
```

**API Documentation:**

```text
/docs
/redoc
```

**Application Run Command:**

```bash
python -m uvicorn app.main:app --reload
```

---

# 57. Author

**Palak Ganwani**

Backend & Database Intern

**Infosys Springboard Virtual Internship 7.0**

**MarketMind AI – Small Business Sales Intelligence Platform**
