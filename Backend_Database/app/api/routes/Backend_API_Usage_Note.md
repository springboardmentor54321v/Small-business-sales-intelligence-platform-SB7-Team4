MarketMind AI Backend – API Usage Note

Project Overview
The MarketMind AI Backend is developed using FastAPI, PostgreSQL, SQLAlchemy, and Pydantic. It provides REST APIs for managing sales data, inventory, invoices, payments, and revenue reporting. All APIs have been tested using Swagger UI and Postman, and the responses have been verified against the PostgreSQL database.
________________________________________

1. Sales Upload API
Endpoint: POST /api/sales/upload
This API accepts a CSV file containing sales data. The uploaded file is validated for file type and required columns before processing. If the schema is valid, the API returns the file details and validation status; otherwise, it returns appropriate validation errors.
Purpose: Initial sales data upload and validation.
________________________________________
2. Inventory APIs
Endpoints:
•	GET /inventory 
•	GET /inventory/{product_id} 
•	POST /inventory 
•	PUT /inventory/{product_id} 
•	DELETE /inventory/{product_id} 
These APIs manage product inventory. Users can retrieve all inventory records, view a single product's stock, create new inventory entries, update stock quantities, or delete inventory records. Inventory is also automatically updated when invoices are created.
Purpose: Inventory management and stock monitoring.
________________________________________
3. Sales Transaction APIs
Endpoints:
•	GET /sales 
•	GET /sales/{transaction_id} 
•	POST /sales 
•	PUT /sales/{transaction_id} 
•	DELETE /sales/{transaction_id} 
These APIs manage sales transactions. New transactions automatically validate available inventory before reducing stock quantities. Pagination has been implemented for the GET All Sales endpoint because the dataset contains over 51,000 records, improving performance and reducing response time.
Purpose: Record and manage product sales.
________________________________________
4. Invoice APIs
Endpoints:
•	GET /invoices 
•	GET /invoices/{invoice_id} 
•	POST /invoices 
•	PUT /invoices/{invoice_id} 
•	DELETE /invoices/{invoice_id} 
Additional Filters
•	payment_status 
•	customer_id 
•	invoice_number 
Invoice creation validates customers, stores, products, and inventory availability. The system automatically calculates subtotal, tax, total amount, generates a unique invoice number, creates invoice items, and updates inventory quantities.
Purpose: Complete invoice lifecycle management.
________________________________________
5. Payment APIs
Endpoints:
•	GET /payments/{invoice_id} 
•	POST /payments 
•	PUT /payments/{payment_id} 
•	DELETE /payments/{payment_id} 
These APIs record and manage invoice payments. Multiple payments can be recorded against a single invoice, enabling support for partial payments. The invoice payment status is automatically updated (Pending, Partially Paid, or Paid) based on the cumulative amount received.
Purpose: Payment tracking and invoice settlement.
________________________________________
6. Revenue Summary API
Endpoint: GET /revenue/summary
This API provides dashboard-level financial metrics by calculating:
•	Total Revenue 
•	Total Outstanding Amount 
•	Daily Collections 
The returned values are computed directly from the Invoice and Payment tables, ensuring consistency with the database.
Purpose: Business revenue analytics and dashboard reporting.
________________________________________

Testing Summary
•	All APIs tested successfully using Swagger UI. 
•	End-to-end API validation completed using Postman. 
•	Database values verified with PostgreSQL. 
•	Pagination implemented only for the Sales Transaction API due to the large dataset. 
•	Invoice, Payment, Revenue, Inventory, and Sales Upload APIs were verified to work correctly. 
________________________________________

Conclusion
The backend implementation for MarketMind AI Milestone 2 has been successfully completed. All APIs have been developed, tested, and validated according to the SRS requirements. The backend is ready for frontend integration and final system testing with the Security API Gateway and AI/ML modules.
