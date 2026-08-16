from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Numeric,
    TIMESTAMP,
    text
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    invoice_item_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    invoice_id = Column(
        String(30),
        ForeignKey("invoices.invoice_id"),
        nullable=False
    )

    product_id = Column(
        String(20),
        ForeignKey("products.product_id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    unit_price = Column(
        Numeric(10, 2),
        nullable=False
    )

    discount = Column(
        Numeric(10, 2),
        nullable=False,
        default=0.00
    )

    tax = Column(
        Numeric(10, 2),
        nullable=False,
        default=0.00
    )

    line_total = Column(
        Numeric(10, 2),
        nullable=False
    )

    category_snapshot = Column(
        String(100),
        nullable=False
    )

    product_name_snapshot = Column(
        String(255),
        nullable=False
    )

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

    invoice = relationship(
        "Invoice",
        back_populates="invoice_items"
    )

    product = relationship(
        "Product",
        back_populates="invoice_items"
    )
