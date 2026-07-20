CREATE TABLE invoices (
    invoice_id VARCHAR(30) PRIMARY KEY,
    invoice_number VARCHAR(30) UNIQUE NOT NULL,

    customer_id VARCHAR(50) NOT NULL,
    store_id VARCHAR(50) NOT NULL,
    created_by_user_id INT NOT NULL,

    invoice_date DATE NOT NULL,
    due_date DATE NOT NULL,

    subtotal NUMERIC(12,2) NOT NULL CHECK (subtotal >= 0),
    discount_amount NUMERIC(12,2) DEFAULT 0 CHECK (discount_amount >= 0),
    tax_amount NUMERIC(12,2) DEFAULT 0 CHECK (tax_amount >= 0),
    total_amount NUMERIC(12,2) NOT NULL CHECK (total_amount >= 0),

    payment_status VARCHAR(30) NOT NULL,
    invoice_status VARCHAR(30) NOT NULL,

    notes VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_invoice_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_invoice_store
        FOREIGN KEY (store_id)
        REFERENCES stores(store_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_invoice_user
        FOREIGN KEY (created_by_user_id)
        REFERENCES users(id)
        ON DELETE RESTRICT
);


CREATE TABLE invoice_items (
    invoice_item_id SERIAL PRIMARY KEY,

    invoice_id VARCHAR(30) NOT NULL,
    product_id VARCHAR(50) NOT NULL,

    quantity INT NOT NULL CHECK (quantity > 0),

    unit_price NUMERIC(10,2) NOT NULL CHECK (unit_price >= 0),

    discount NUMERIC(10,2) DEFAULT 0 CHECK (discount >= 0),

    tax NUMERIC(10,2) DEFAULT 0 CHECK (tax >= 0),

    line_total NUMERIC(12,2) NOT NULL CHECK (line_total >= 0),

    category_snapshot VARCHAR(100) NOT NULL,

    product_name_snapshot VARCHAR(255) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_invoiceitem_invoice
        FOREIGN KEY (invoice_id)
        REFERENCES invoices(invoice_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_invoiceitem_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
        ON DELETE RESTRICT
);


CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,

    invoice_id VARCHAR(30) NOT NULL,

    payment_date DATE NOT NULL,

    amount_paid NUMERIC(12,2) NOT NULL CHECK (amount_paid >= 0),

    payment_method VARCHAR(50) NOT NULL,

    transaction_reference VARCHAR(100),

    remarks VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_payment_invoice
        FOREIGN KEY (invoice_id)
        REFERENCES invoices(invoice_id)
        ON DELETE CASCADE
);
