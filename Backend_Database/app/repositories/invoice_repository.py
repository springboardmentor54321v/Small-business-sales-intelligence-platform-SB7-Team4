from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.invoice import Invoice

from typing import Optional

from sqlalchemy import func

def get_all_invoices(
    db: Session,
    payment_status: Optional[str] = None,
    customer_id: Optional[str] = None,
    invoice_number: Optional[str] = None
):

    query = db.query(Invoice)

    

    if payment_status:
        query = query.filter(
            func.lower(Invoice.payment_status) == payment_status.lower()
        )

    if customer_id:
        query = query.filter(
            func.lower(Invoice.customer_id) == customer_id.lower()
        )

    if invoice_number:
        query = query.filter(
            func.lower(Invoice.invoice_number) == invoice_number.lower()
        )

    return query.all()

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
