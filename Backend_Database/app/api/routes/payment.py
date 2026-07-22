from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.payment import (
    PaymentCreate,
    PaymentUpdate,
    PaymentResponse,
)

from app.repositories.payment_repository import (
    get_all_payments,
    get_payment_by_payment_id,
    update_payment,
    delete_payment,
)

from app.services.payment_service import (
    process_payment,
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


# =====================================================
# Get All Payments
# =====================================================

@router.get(
    "/",
    response_model=list[PaymentResponse]
)
def get_payments(
    db: Session = Depends(get_db)
):

    return get_all_payments(db)


# =====================================================
# Get Payment By ID
# =====================================================

@router.get(
    "/{payment_id}",
    response_model=PaymentResponse
)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):

    return get_payment_by_payment_id(
        db,
        payment_id
    )


# =====================================================
# Create Payment
# =====================================================

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
def add_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db)
):

    return process_payment(
        db,
        payment
    )


# =====================================================
# Update Payment
# =====================================================

@router.put(
    "/{payment_id}",
    response_model=PaymentResponse
)
def edit_payment(
    payment_id: int,
    payment: PaymentUpdate,
    db: Session = Depends(get_db)
):

    return update_payment(
        db,
        payment_id,
        payment
    )


# =====================================================
# Delete Payment
# =====================================================

@router.delete("/{payment_id}")
def remove_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):

    return delete_payment(
        db,
        payment_id
    )
