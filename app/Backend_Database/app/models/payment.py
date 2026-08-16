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


class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    invoice_id = Column(
        String(30),
        ForeignKey("invoices.invoice_id"),
        nullable=False
    )

    payment_date = Column(
        Date,
        nullable=False
    )

    amount_paid = Column(
        Numeric(10, 2),
        nullable=False
    )

    payment_method = Column(
        String(50),
        nullable=False
    )

    transaction_reference = Column(
        String(100),
        nullable=True
    )

    remarks = Column(
        String(255),
        nullable=True
    )

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

    invoice = relationship(
        "Invoice",
        back_populates="payments"
    )
