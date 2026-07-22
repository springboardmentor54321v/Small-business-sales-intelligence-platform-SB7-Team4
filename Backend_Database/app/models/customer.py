from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(String(20), unique=True, nullable=False)

    name = Column(String(100), nullable=False)

    email = Column(String(100), unique=True)

    phone = Column(String(20))

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

    # Relationship with SalesTransaction
    sales_transactions = relationship(
        "SalesTransaction",
        back_populates="customer"
    )

    # Relationship with Invoice
    invoices = relationship(
        "Invoice",
        back_populates="customer"
    )
