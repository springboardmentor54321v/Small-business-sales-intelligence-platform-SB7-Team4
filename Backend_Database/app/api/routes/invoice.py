from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.invoice import (
    InvoiceCreate,
    InvoiceUpdate,
    InvoiceResponse,
)

from app.repositories.invoice_repository import (
    get_all_invoices,
    get_invoice_by_invoice_id,
    update_invoice,
    delete_invoice,
)

from app.services.invoice_service import (
    create_invoice_service,
)

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)

from typing import Optional
from fastapi import Query

# =====================================================
# Get All Invoices
# =====================================================

@router.get(
    "/",
    response_model=list[InvoiceResponse]
)
def get_invoices(
    payment_status: Optional[str] = Query(None),
    customer_id: Optional[str] = Query(None),
    invoice_number: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):

    return get_all_invoices(
        db,
        payment_status,
        customer_id,
        invoice_number
    )

# =====================================================
# Get Invoice By ID
# =====================================================

@router.get(
    "/{invoice_id}",
    response_model=InvoiceResponse
)
def get_invoice(
    invoice_id: str,
    db: Session = Depends(get_db)
):

    return get_invoice_by_invoice_id(
        db,
        invoice_id
    )

# =====================================================
# Create Invoice
# =====================================================

@router.post(
    "/",
    response_model=InvoiceResponse,
    status_code=status.HTTP_201_CREATED
)
def create_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db)
):

    return create_invoice_service(
        db,
        invoice
    )

# =====================================================
# Update Invoice
# =====================================================

@router.put(
    "/{invoice_id}",
    response_model=InvoiceResponse
)
def edit_invoice(
    invoice_id: str,
    invoice: InvoiceUpdate,
    db: Session = Depends(get_db)
):

    return update_invoice(
        db,
        invoice_id,
        invoice
    )

# =====================================================
# Delete Invoice
# =====================================================

@router.delete("/{invoice_id}")
def remove_invoice(
    invoice_id: str,
    db: Session = Depends(get_db)
):

    return delete_invoice(
        db,
        invoice_id
    )
