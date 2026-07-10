from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.inventory import Inventory
from app.models.sales_transaction import SalesTransaction


# =====================================================
# Get All Sales
# =====================================================

def get_all_sales(db: Session):
    return db.query(SalesTransaction).all()


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
