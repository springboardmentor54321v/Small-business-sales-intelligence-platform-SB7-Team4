from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)

    store_id = Column(String(20), unique=True, nullable=False)

    store_name = Column(String(100), nullable=False)

    location = Column(String(255))

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

    sales_transactions = relationship(
        "SalesTransaction",
        back_populates="store"
    )

    invoices = relationship(
        "Invoice",
        back_populates="store"
    )
