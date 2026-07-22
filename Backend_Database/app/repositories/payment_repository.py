from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.payment import Payment

def get_all_payments(db: Session):

    return db.query(Payment).all()

def get_payment_by_payment_id(
    db: Session,
    payment_id: int
):

    payment = (
        db.query(Payment)
        .filter(
            Payment.payment_id == payment_id
        )
        .first()
    )

    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found."
        )

    return payment

def get_payment_by_invoice(
    db: Session,
    invoice_id: str
):

    payments = (
        db.query(Payment)
        .filter(
            Payment.invoice_id == invoice_id
        )
        .all()
    )

    if not payments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No payment records found."
        )

    return payments

def create_payment(
    db: Session,
    payment
):

    new_payment = Payment(
        invoice_id=payment.invoice_id,
        payment_date=payment.payment_date,
        amount_paid=payment.amount_paid,
        payment_method=payment.payment_method,
        transaction_reference=payment.transaction_reference,
        remarks=payment.remarks
    )

    db.add(new_payment)

    db.commit()

    db.refresh(new_payment)

    return new_payment

def update_payment(
    db: Session,
    payment_id: int,
    updated_payment
):

    payment = (
        db.query(Payment)
        .filter(
            Payment.payment_id == payment_id
        )
        .first()
    )

    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found."
        )

    update_data = updated_payment.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(payment, key, value)

    db.commit()

    db.refresh(payment)

    return payment


def delete_payment(
    db: Session,
    payment_id: int
):

    payment = (
        db.query(Payment)
        .filter(
            Payment.payment_id == payment_id
        )
        .first()
    )

    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found."
        )

    db.delete(payment)

    db.commit()

    return {
        "message": "Payment deleted successfully."
    }
