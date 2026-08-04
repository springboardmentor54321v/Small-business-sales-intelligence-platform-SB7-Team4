from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.invoice import Invoice

from typing import Optional

from sqlalchemy import func

def get_all_invoices(

    db: Session,

    page: int = 1,

    page_size: int = 10,

    payment_status: Optional[str] = None,

    invoice_status: Optional[str] = None,

    customer_id: Optional[str] = None,

    invoice_number: Optional[str] = None,

):

    query = db.query(Invoice)

    # ==========================
    # Payment Status
    # ==========================

    if payment_status:

        query = query.filter(
            func.lower(Invoice.payment_status)
            == payment_status.lower()
        )

    # ==========================
    # Invoice Status
    # ==========================

    if invoice_status:

        query = query.filter(
            func.lower(Invoice.invoice_status)
            == invoice_status.lower()
        )

    # ==========================
    # Customer
    # ==========================

    if customer_id:

        query = query.filter(
            func.lower(Invoice.customer_id)
            == customer_id.lower()
        )

    # ==========================
    # Invoice Number Search
    # ==========================

    if invoice_number:

        query = query.filter(
            Invoice.invoice_number.ilike(f"%{invoice_number}%")
        )

    invoices = (

        query
        .order_by(Invoice.invoice_date.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()

    )

    return invoices

def get_invoice_by_invoice_id(
    db: Session,
    invoice_id: str
):

    invoice = (
        db.query(Invoice)
        .filter(
            Invoice.invoice_id == invoice_id
        )
        .first()
    )

    if invoice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found."
        )

    return invoice


def generate_invoice_number(db: Session):

    latest_invoice = (
        db.query(Invoice)
        .order_by(Invoice.invoice_number.desc())
        .first()
    )

    if latest_invoice is None:
        return "INV900001"

    latest_number = int(
        latest_invoice.invoice_number.replace("INV", "")
    )

    return f"INV{latest_number + 1:06d}"


def create_invoice(
    db: Session,
    invoice_data: dict
):

    new_invoice = Invoice(**invoice_data)

    db.add(new_invoice)

    db.commit()

    db.refresh(new_invoice)

    return new_invoice


def update_invoice(
    db: Session,
    invoice_id: str,
    updated_invoice
):

    invoice = (
        db.query(Invoice)
        .filter(
            Invoice.invoice_id == invoice_id
        )
        .first()
    )

    if invoice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found."
        )

    update_data = updated_invoice.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(invoice, key, value)

    db.commit()

    db.refresh(invoice)

    return invoice

# =====================================================
# Bulk Update Invoices
# =====================================================

def bulk_update_invoices(
    db: Session,
    invoice_ids: list[str],
    payment_status: str,
):

    if not invoice_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No invoice IDs provided."
        )

    invoices = (
        db.query(Invoice)
        .filter(
            Invoice.invoice_id.in_(invoice_ids)
        )
        .all()
    )

    if len(invoices) != len(invoice_ids):

        found_ids = {
            invoice.invoice_id
            for invoice in invoices
        }

        missing_ids = [
            invoice_id
            for invoice_id in invoice_ids
            if invoice_id not in found_ids
        ]

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "Invoice(s) not found: "
                + ", ".join(missing_ids)
            )
        )

    for invoice in invoices:

        invoice.payment_status = payment_status

    try:
        db.commit()

        return {
            "updated_count": len(invoices),
            "message": "Invoices updated successfully."
        }
    
    except Exception:
        db.rollback()
        raise

def delete_invoice(
    db: Session,
    invoice_id: str
):

    invoice = (
        db.query(Invoice)
        .filter(
            Invoice.invoice_id == invoice_id
        )
        .first()
    )

    if invoice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found."
        )

    db.delete(invoice)

    db.commit()

    return {
        "message": "Invoice deleted successfully."
    }
