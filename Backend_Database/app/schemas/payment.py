from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


# =====================================================
# Base Schema
# =====================================================

class PaymentBase(BaseModel):
    invoice_id: str
    payment_date: date
    amount_paid: Decimal
    payment_method: str
    transaction_reference: Optional[str] = None
    remarks: Optional[str] = None


# =====================================================
# Create Schema
# =====================================================

class PaymentCreate(PaymentBase):
    pass


# =====================================================
# Update Schema
# =====================================================

class PaymentUpdate(BaseModel):
    payment_date: Optional[date] = None
    amount_paid: Optional[Decimal] = None
    payment_method: Optional[str] = None
    transaction_reference: Optional[str] = None
    remarks: Optional[str] = None


# =====================================================
# Response Schema
# =====================================================

class PaymentResponse(PaymentBase):
    payment_id: int

    model_config = ConfigDict(from_attributes=True)
