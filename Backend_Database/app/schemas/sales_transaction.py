from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SalesTransactionBase(BaseModel):
    transaction_id: str
    invoice_id: str
    transaction_date: date
    customer_id: str
    product_id: str
    store_id: str
    quantity: int
    unit_price: Decimal
    discount: Decimal
    total_amount: Decimal
    payment_method: Optional[str] = None
    created_by_user_id: int


class SalesTransactionCreate(SalesTransactionBase):
    pass


class SalesTransactionUpdate(BaseModel):
    quantity: Optional[int] = None
    discount: Optional[Decimal] = None
    total_amount: Optional[Decimal] = None
    payment_method: Optional[str] = None


class SalesTransactionResponse(SalesTransactionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
