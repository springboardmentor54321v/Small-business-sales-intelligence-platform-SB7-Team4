from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    product_id: str
    product_name: str
    category: str
    unit_price: Decimal


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    category: Optional[str] = None
    unit_price: Optional[Decimal] = None


class ProductResponse(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
