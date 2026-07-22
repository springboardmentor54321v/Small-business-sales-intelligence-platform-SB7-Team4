from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.invoice import Invoice
from app.models.payment import Payment

from app.repositories.payment_repository import (
    create_payment
)

# =====================================================
# Validate Invoice
# =====================================================

def validate_invoice(
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

from sqlalchemy import func


# =====================================================
# Calculate Total Amount Paid
# =====================================================

def calculate_total_paid(
    db: Session,
    invoice_id: str
):

    total_paid = (
        db.query(
            func.sum(Payment.amount_paid)
        )
        .filter(
            Payment.invoice_id == invoice_id
        )
        .scalar()
    )

    return total_paid or 0

# =====================================================
# Update Invoice Payment Status
# =====================================================

def update_invoice_payment_status(
    invoice: Invoice,
    total_paid
):

    if total_paid <= 0:

        invoice.payment_status = "Pending"
        invoice.invoice_status = "Generated"

    elif total_paid < invoice.total_amount:

        invoice.payment_status = "Partially Paid"
        invoice.invoice_status = "Generated"

    else:

        invoice.payment_status = "Paid"
        invoice.invoice_status = "Completed"

# =====================================================
# Check Overdue Invoice
# =====================================================

def check_overdue_invoice(
    invoice: Invoice
):

    if (
        invoice.due_date < date.today()
        and invoice.payment_status != "Paid"
    ):

        return True

    return False

# =====================================================
# Process Payment
# =====================================================

def process_payment(
    db: Session,
    payment
):

    # -----------------------------
    # Validate Invoice
    # -----------------------------
    invoice = validate_invoice(
        db,
        payment.invoice_id
    )

    # -----------------------------
    # Create Payment Record
    # -----------------------------
    payment_record = create_payment(
        db,
        payment
    )

    # -----------------------------
    # Calculate Total Amount Paid
    # -----------------------------
    total_paid = calculate_total_paid(
        db,
        payment.invoice_id
    )

    # -----------------------------
    # Update Invoice Status
    # -----------------------------
    update_invoice_payment_status(
        invoice,
        total_paid
    )

    db.commit()

    db.refresh(invoice)

    # -----------------------------
    # Check Reminder
    # -----------------------------
    reminder = check_overdue_invoice(
        invoice
    )

    return {
        "payment": payment_record,
        "invoice_status": invoice.payment_status,
        "invoice_total": invoice.total_amount,
        "total_paid": total_paid,
        "remaining_amount": max(invoice.total_amount - total_paid,0),
        "reminder": reminder
    }
