from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP, text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(String(20), unique=True, nullable=False)

    product_name = Column(String(255), nullable=False)

    category = Column(String(100))

    unit_price = Column(Numeric(10, 2), nullable=False)

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )

    inventory = relationship(
        "Inventory",
        back_populates="product",
        uselist=False
    )

    sales_transactions = relationship(
        "SalesTransaction",
        back_populates="product"
    )
    
