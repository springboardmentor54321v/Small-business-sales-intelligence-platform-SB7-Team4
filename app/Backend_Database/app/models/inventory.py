from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(
        String(50),
        ForeignKey("products.product_id"),
        nullable=False,
        unique=True
    )

    stock_quantity = Column(Integer, nullable=False)

    low_stock_threshold = Column(Integer, nullable=False)

    updated_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP")
    )

    product = relationship(
        "Product",
        back_populates="inventory"
    )
   
