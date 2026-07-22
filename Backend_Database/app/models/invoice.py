from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
    Numeric,
    TIMESTAMP,
    text
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class Invoice(Base):
    __tablename__ = "invoices"

    invoice_id = Column(
        String(30),
        primary_key=True,
        unique=True,
        nullable=False
    )

    invoice_number = Column(
        String(30),
        unique=True,
        nullable=False
    )

    customer_id = Column(
        String(20),
        ForeignKey("customers.customer_id"),
        nullable=False
    )

    store_id = Column(
        String(20),
        ForeignKey("stores.store_id"),
        nullable=False
    )

    created_by_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    invoice_date = Column(
        Date,
        nullable=False
    )

    due_date = Column(
        Date,
        nullable=False
    )

    subtotal = Column(
        Numeric(10, 2),
        nullable=False
    )

    discount_amount = Column(
        Numeric(10, 2),
        nullable=False,
        default=0.00
    )

    tax_amount = Column(
        Numeric(10, 2),
        nullable=False,
        default=0.00
    )

    total_amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    payment_status = Column(
        String(30),
        nullable=False
    )

    invoice_status = Column(
        String(30),
        nullable=False
    )

    notes = Column(
        String(255),
        nullable=True
    )

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

    updated_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP")
    )

    customer = relationship(
        "Customer",
        back_populates="invoices"
    )

    store = relationship(
        "Store",
        back_populates="invoices"
    )

    created_by = relationship(
        "User",
        back_populates="invoices"
    )

    invoice_items = relationship(
        "InvoiceItem",
        back_populates="invoice",
        cascade="all, delete-orphan"
    )

    payments = relationship(
        "Payment",
        back_populates="invoice",
        cascade="all, delete-orphan"
    )

    sales_transactions = relationship(
        "SalesTransaction",
        back_populates="invoice"
    )
    
