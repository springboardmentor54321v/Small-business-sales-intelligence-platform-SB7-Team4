# MarketMind AI Backend – API Usage Note

## Project Overview

The **MarketMind AI Backend** is developed using **FastAPI, PostgreSQL, SQLAlchemy, and Pydantic**. It provides REST APIs for sales data ingestion, customer management, inventory management, sales transactions, invoices, payments, revenue reporting, and notifications.

The backend supports CSV-based sales ingestion with automatic column detection/mapping and ETL processing. It also provides validation, pagination, filtering, inventory updates, invoice/payment workflows, revenue calculations, and notification logic.

All implemented APIs have been manually tested through **Swagger UI/Postman**, verified against the PostgreSQL database, and the automated test suite currently passes **31/31 tests**.

---

# 1. Sales Upload API

## Endpoint

```http
POST /api/sales/upload
```

## Description

Accepts a sales CSV file and automatically:

- Validates that the uploaded file is a CSV
- Reads and validates the CSV
- Detects and maps supported column names/aliases
- Normalizes the sales data
- Resolves the store using `store_id` or CSV location information
- Performs ETL processing
- Imports valid sales data into the database
- Creates corresponding invoice and invoice-item records when applicable
- Reports inserted and skipped rows

## Purpose

- Sales data ingestion
- Automatic CSV normalization
- ETL processing
- Database import

## Validation

The API rejects:

- Non-CSV files
- Empty CSV files
- Invalid CSV files
- Invalid/insufficient CSV structure
- CSV locations that cannot be matched to an existing store

---

# 2. Customer APIs

## Endpoints

```http
GET    /customers/
POST   /customers/
DELETE /customers/{customer_id}
```

## GET Customers

Supports:

- Pagination
- Customer search

Query parameters:

```text
page
page_size
search
```

## POST Customer

Creates a new customer.

Validation includes:

- Customer ID cannot be empty
- Customer name cannot be empty
- Email, when provided, must have a valid format
- Phone, when provided, cannot be empty
- Duplicate Customer IDs are rejected

## DELETE Customer

Deletes a customer only when the customer has no historical business records.

Customers with:

- Sales transaction history
- Invoice history

cannot be deleted. This prevents accidental deletion of historical sales and financial data.

## Purpose

- Customer management
- Customer search
- Customer data integrity
- Protection of historical business records

---

# 3. Inventory APIs

## Endpoints

```http
GET    /inventory/
GET    /inventory/{product_id}
POST   /inventory/
PUT    /inventory/{product_id}
PUT    /inventory/bulk-update
DELETE /inventory/{product_id}
```

## GET Inventory

Supports:

- Pagination
- Search by Product ID
- Search by Product Name
- Category filtering
- Ordered inventory results

Query parameters:

```text
page
page_size
category
search
```

## POST Inventory

Creates an inventory record for a product.

Duplicate inventory records for the same product are rejected.

## PUT Inventory

Updates:

- Stock quantity
- Low-stock threshold

## Bulk Update Inventory

Multiple inventory records can be updated in a single request.

The API validates that:

- Updates are provided
- The specified product exists

## DELETE Inventory

Deletes the inventory record associated with a product.

## Purpose

- Inventory management
- Stock monitoring
- Low-stock threshold management
- Bulk stock updates
- Inventory search/filtering

---

# 4. Sales Transaction APIs

## Endpoints

```http
GET    /sales/
GET    /sales/{transaction_id}
POST   /sales/
PUT    /sales/{transaction_id}
DELETE /sales/{transaction_id}
```

## Description

These APIs manage sales transactions and synchronize sales with inventory.

## POST Sales Transaction

The final workflow:

- Validates the customer
- Validates the product
- Validates the invoice when applicable
- Obtains the product's unit price from product data
- Accepts the applicable discount
- Calculates the transaction total amount
- Checks available inventory
- Creates the sales transaction
- Reduces inventory after a successful sale

The frontend does not need to manually provide the authoritative product unit price or calculate the final total amount.

## PUT Sales Transaction

Updates a sales transaction while correctly adjusting inventory based on the quantity change.

For example, changing a transaction quantity from `2` to `5` adjusts inventory by the additional quantity of `3`.

## DELETE Sales Transaction

Deletes the specified sales transaction.

## Validation

The API handles invalid:

- Transaction IDs
- Product IDs
- Customer IDs
- Invoice IDs
- Inventory availability

with controlled API errors.

## Purpose

- Sales transaction management
- Accurate transaction totals
- Inventory synchronization
- Historical transaction records

---

# 5. Invoice APIs

## Endpoints

```http
GET    /invoices/
GET    /invoices/{invoice_id}
POST   /invoices/
PUT    /invoices/{invoice_id}
DELETE /invoices/{invoice_id}
```

## Additional Filters

Invoice retrieval supports filtering using available API parameters such as:

- `payment_status`
- `customer_id`
- `invoice_number`

## Invoice Creation

Invoice creation performs the following operations:

- Validates customer
- Validates store
- Validates products
- Checks inventory availability
- Generates a unique invoice number
- Calculates subtotal
- Applies discount information
- Calculates tax
- Calculates total amount
- Creates invoice items
- Updates inventory

## Purpose

- Complete invoice lifecycle management
- Invoice calculation
- Invoice-item management
- Inventory synchronization
- Payment workflow support

---

# 6. Payment APIs

## Endpoints

```http
GET    /payments/
GET    /payments/{payment_id}
POST   /payments/
PUT    /payments/{payment_id}
DELETE /payments/{payment_id}
```

## Description

Payment APIs record and manage payments against invoices.

The system supports:

- Multiple payments for one invoice
- Partial payments
- Cumulative payment calculation
- Automatic invoice payment-status updates
- Remaining amount calculation
- Overdue invoice reminder determination

## Payment Statuses

```text
Pending
Partially Paid
Paid
```

## Payment Workflow

When a payment is created:

1. The invoice is validated.
2. The payment is recorded.
3. Total amount paid for the invoice is calculated.
4. Invoice payment status is updated.
5. Invoice status is updated when fully paid.
6. Remaining amount is calculated.
7. Overdue reminder status is determined.

## Purpose

- Payment tracking
- Invoice settlement
- Partial-payment management
- Automatic payment status updates
- Overdue payment identification

---

# 7. Revenue Summary API

## Endpoint

```http
GET /revenue/summary
```

## Description

Provides dashboard-level business metrics:

- Total Revenue
- Total Outstanding Amount
- Daily Collections

The values are calculated from Invoice and Payment data to maintain consistency with the database.

## Purpose

- Revenue analytics
- Dashboard reporting
- Outstanding payment monitoring
- Collection tracking

---

# 8. Notification API

## Endpoint

```http
GET /notifications
```

## Description

Provides application notifications generated from business conditions.

Notification logic includes:

- Inventory stock severity
- Overdue invoice severity

## Inventory Severity

Possible severity levels include:

```text
CRITICAL
HIGH
MEDIUM
```

## Invoice Severity

Possible severity levels include:

```text
MEDIUM
HIGH
CRITICAL
```

## Purpose

- Low-stock notifications
- Overdue invoice notifications
- Business alerts
- Dashboard notifications

---

# 9. API Validation and Error Handling

The backend includes controlled validation for common invalid requests.

Examples include:

```text
400 Bad Request
404 Not Found
409 Conflict
422 Unprocessable Content
```

Examples:

- Duplicate customer → `400`
- Duplicate inventory → `400`
- Nonexistent customer → `404`
- Nonexistent product → `404`
- Customer with historical records → `409`
- Invalid customer input → `422`
- Invalid CSV upload → `400`

The backend is designed to return controlled errors rather than unexpected internal server errors for expected invalid requests.

---

# 10. Automated Testing

The backend contains an automated test suite using **pytest**.

Current result:

```text
31 tests
31 passed
0 failed
```

The tests cover:

- Customer API
- Inventory API
- Sales transaction API
- Invoice functionality
- Payment functionality
- Revenue summary
- Notification logic
- Sales CSV upload validation
- API integration

Run all automated tests with:

```bash
pytest -v
```

---

# 11. API Testing

The APIs have been manually tested using:

- Swagger UI
- Postman
- PostgreSQL database verification

## Verified Areas

- Sales Upload and ETL
- Customer management
- Inventory management
- Sales transactions
- Invoice workflow
- Payment workflow
- Revenue calculations
- Notifications
- Search and filtering
- Pagination
- Error handling
- Inventory synchronization

---


# 14. Final API Overview

| Module | Main Endpoints |
|---|---|
| Sales Upload | `POST /api/sales/upload` |
| Customers | `GET /customers/`, `POST /customers/`, `DELETE /customers/{customer_id}` |
| Inventory | `GET`, `POST`, `PUT`, bulk update, `DELETE` |
| Sales Transactions | `GET`, `POST`, `PUT`, `DELETE` |
| Invoices | `GET`, `POST`, `PUT`, `DELETE` |
| Payments | `GET`, `POST`, `PUT`, `DELETE` |
| Revenue | `GET /revenue/summary` |
| Notifications | `GET /notifications` |

---

# Conclusion

The **MarketMind AI Backend** now provides the backend functionality developed across the project milestones, including sales ingestion/ETL, customer management, inventory management, sales transactions, invoice and payment workflows, revenue reporting, and notifications.

The backend has undergone manual API testing, database verification, error-handling validation, and automated testing with **31/31 tests passing**.
