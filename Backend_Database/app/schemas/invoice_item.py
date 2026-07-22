from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


# =====================================================
# Base Schema
# =====================================================

class InvoiceItemBase(BaseModel):
    product_id: str
    quantity: int


# =====================================================
# Create Schema
# =====================================================

class InvoiceItemCreate(InvoiceItemBase):
    pass


# =====================================================
# Update Schema
# =====================================================

class InvoiceItemUpdate(BaseModel):
    quantity: Optional[int] = None


# =====================================================
# Response Schema
# =====================================================

class InvoiceItemResponse(InvoiceItemBase):
    invoice_item_id: int

    unit_price: Decimal
    discount: Decimal
    tax: Decimal
    line_total: Decimal

    category_snapshot: str
    product_name_snapshot: str

    model_config = ConfigDict(from_attributes=True)
