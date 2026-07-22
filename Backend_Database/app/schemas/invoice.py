from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.invoice_item import InvoiceItemCreate


# =====================================================
# Base Schema
# =====================================================

class InvoiceBase(BaseModel):
    customer_id: str
    store_id: str
    created_by_user_id: int
    invoice_date: date
    due_date: date
    notes: Optional[str] = None


# =====================================================
# Create Schema
# =====================================================

class InvoiceCreate(InvoiceBase):
    items: list[InvoiceItemCreate]


# =====================================================
# Update Schema
# =====================================================

class InvoiceUpdate(BaseModel):
    due_date: Optional[date] = None
    payment_status: Optional[str] = None
    invoice_status: Optional[str] = None
    notes: Optional[str] = None


# =====================================================
# Response Schema
# =====================================================

class InvoiceResponse(InvoiceBase):
    invoice_id: str
    invoice_number: str

    subtotal: Decimal
    discount_amount: Decimal
    tax_amount: Decimal
    total_amount: Decimal

    payment_status: str
    invoice_status: str

    model_config = ConfigDict(from_attributes=True)
