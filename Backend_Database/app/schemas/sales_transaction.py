from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


# =====================================================
# Create Schema
# =====================================================

class SalesTransactionCreate(BaseModel):
    transaction_id: str
    invoice_id: str
    transaction_date: date
    customer_id: str
    product_id: str
    store_id: str
    quantity: int
    discount: Decimal
    payment_method: Optional[str] = None
    created_by_user_id: int


# =====================================================
# Update Schema
# =====================================================

class SalesTransactionUpdate(BaseModel):
    quantity: Optional[int] = None
    discount: Optional[Decimal] = None
    payment_method: Optional[str] = None


# =====================================================
# Response Schema
# =====================================================

class SalesTransactionResponse(BaseModel):
    transaction_id: str
    invoice_id: str
    transaction_date: date
    customer_id: str
    product_id: str
    store_id: str
    quantity: int

    # These are returned by the backend
    unit_price: Decimal
    discount: Decimal
    total_amount: Decimal

    payment_method: Optional[str] = None
    created_by_user_id: int

    id: int
    product_name: str
    category: str

    model_config = ConfigDict(from_attributes=True)
