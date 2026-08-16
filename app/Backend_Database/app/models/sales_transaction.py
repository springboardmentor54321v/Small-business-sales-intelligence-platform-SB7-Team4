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


class SalesTransaction(Base):
    __tablename__ = "sales_transactions"

    id = Column(Integer, primary_key=True, index=True)

    transaction_id = Column(String(30), unique=True, nullable=False)

    invoice_id = Column(
        String(30),
        ForeignKey("invoices.invoice_id"),
        nullable=False
    )

    transaction_date = Column(Date, nullable=False)

    customer_id = Column(
        String(50),
        ForeignKey("customers.customer_id"),
        nullable=False
    )

    product_id = Column(
        String(50),
        ForeignKey("products.product_id"),
        nullable=False
    )

    store_id = Column(
        String(50),
        ForeignKey("stores.store_id"),
        nullable=False
    )

    quantity = Column(Integer, nullable=False)

    unit_price = Column(Numeric(10, 2), nullable=False)

    discount = Column(Numeric(5, 2), nullable=False)

    total_amount = Column(Numeric(10, 2), nullable=False)

    payment_method = Column(String(50), nullable=False)

    created_by_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

    customer = relationship(
        "Customer",
        back_populates="sales_transactions"
    )

    product = relationship(
        "Product",
        back_populates="sales_transactions"
    )

    store = relationship(
        "Store",
        back_populates="sales_transactions"
    )

    user = relationship(
        "User",
        back_populates="sales_transactions"
    )

    invoice = relationship(
        "Invoice",
        back_populates="sales_transactions"
    )
    
