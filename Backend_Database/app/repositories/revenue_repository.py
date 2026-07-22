from datetime import date
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.invoice import Invoice
from app.models.payment import Payment

# =====================================================
# Total Revenue
# =====================================================

def get_total_revenue(
    db: Session
):

    total = (
        db.query(
            func.sum(Payment.amount_paid)
        )
        .scalar()
    )

    return total or Decimal("0.00")

# =====================================================
# Daily Collections
# =====================================================

def get_daily_collections(
    db: Session
):

    total = (
        db.query(
            func.sum(Payment.amount_paid)
        )
        .filter(
            Payment.payment_date == date.today()
        )
        .scalar()
    )

    return total or Decimal("0.00")

# =====================================================
# Total Outstanding
# =====================================================

def get_total_outstanding(
    db: Session
):

    total = (
        db.query(
            func.sum(Invoice.total_amount)
        )
        .filter(
            Invoice.payment_status != "Paid"
        )
        .scalar()
    )

    return total or Decimal("0.00")
