from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.inventory import Inventory
from app.models.sales_transaction import SalesTransaction

from typing import Optional
from datetime import date

from sqlalchemy import or_



# =====================================================
# Get All Sales
# =====================================================

def get_all_sales(

    db: Session,

    page: int = 1,

    page_size: int = 10,

    start_date: Optional[date] = None,

    end_date: Optional[date] = None,

    search: Optional[str] = None,

):

    query = db.query(SalesTransaction)

    # ==========================
    # Date Range Filter
    # ==========================

    if start_date:

        query = query.filter(
            SalesTransaction.transaction_date >= start_date
        )

    if end_date:

        query = query.filter(
            SalesTransaction.transaction_date <= end_date
        )

    # ==========================
    # Search
    # ==========================

    if search:

        query = query.filter(

            or_(

                SalesTransaction.transaction_id.ilike(
                    f"%{search}%"
                ),

                SalesTransaction.invoice_id.ilike(
                    f"%{search}%"
                ),

                SalesTransaction.customer_id.ilike(
                    f"%{search}%"
                ),

                SalesTransaction.product_id.ilike(
                    f"%{search}%"
                ),

            )

        )

    sales = (

        query

        .order_by(
            SalesTransaction.transaction_date.desc()
        )

        .offset((page - 1) * page_size)

        .limit(page_size)

        .all()

    )

    return sales


# =====================================================
# Get Sale By Transaction ID
# =====================================================

def get_sale_by_transaction_id(
    db: Session,
    transaction_id: str
):

    sale = (
        db.query(SalesTransaction)
        .filter(
            SalesTransaction.transaction_id == transaction_id
        )
        .first()
    )

    if sale is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sales transaction not found."
        )

    return sale


# =====================================================
# Create Sale + Reduce Inventory
# =====================================================

def create_sale(
    db: Session,
    sale
):

    inventory = (
        db.query(Inventory)
        .filter(
            Inventory.product_id == sale.product_id
        )
        .first()
    )

    if inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory record not found."
        )

    if inventory.stock_quantity < sale.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient stock available."
        )

    # Reduce stock
    inventory.stock_quantity -= sale.quantity

    new_sale = SalesTransaction(
        transaction_id=sale.transaction_id,
        invoice_id=sale.invoice_id,
        transaction_date=sale.transaction_date,
        customer_id=sale.customer_id,
        product_id=sale.product_id,
        store_id=sale.store_id,
        quantity=sale.quantity,
        unit_price=sale.unit_price,
        discount=sale.discount,
        total_amount=sale.total_amount,
        payment_method=sale.payment_method,
        created_by_user_id=sale.created_by_user_id
    )

    db.add(new_sale)

    db.commit()

    db.refresh(new_sale)

    return new_sale


# =====================================================
# Update Sale
# =====================================================

def update_sale(
    db: Session,
    transaction_id: str,
    updated_sale
):

    sale = (
        db.query(SalesTransaction)
        .filter(
            SalesTransaction.transaction_id == transaction_id
        )
        .first()
    )

    if sale is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sales transaction not found."
        )

    update_data = updated_sale.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(sale, key, value)

    db.commit()

    db.refresh(sale)

    return sale


# =====================================================
# Delete Sale
# =====================================================

def delete_sale(
    db: Session,
    transaction_id: str
):

    sale = (
        db.query(SalesTransaction)
        .filter(
            SalesTransaction.transaction_id == transaction_id
        )
        .first()
    )

    if sale is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sales transaction not found."
        )

    db.delete(sale)

    db.commit()

    return {
        "message": "Sales transaction deleted successfully."
    }
