from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.sales_transaction import (
    SalesTransactionCreate,
    SalesTransactionUpdate,
    SalesTransactionResponse,
)

from app.repositories.sales_transaction_repository import (
    get_all_sales,
    get_sale_by_transaction_id,
    create_sale,
    update_sale,
    delete_sale,
)

router = APIRouter(
    prefix="/sales",
    tags=["Sales Transactions"]
)


# ==================================================
# Get All Sales
# ==================================================

@router.get(
    "/",
    response_model=list[SalesTransactionResponse]
)
def get_sales(
    db: Session = Depends(get_db)
):

    return get_all_sales(db)


# ==================================================
# Get One Sale
# ==================================================

@router.get(
    "/{transaction_id}",
    response_model=SalesTransactionResponse
)
def get_sale(
    transaction_id: str,
    db: Session = Depends(get_db)
):

    return get_sale_by_transaction_id(
        db,
        transaction_id
    )


# ==================================================
# Create Sale
# ==================================================

@router.post(
    "/",
    response_model=SalesTransactionResponse,
    status_code=status.HTTP_201_CREATED
)
def add_sale(
    sale: SalesTransactionCreate,
    db: Session = Depends(get_db)
):

    return create_sale(
        db,
        sale
    )


# ==================================================
# Update Sale
# ==================================================

@router.put(
    "/{transaction_id}",
    response_model=SalesTransactionResponse
)
def edit_sale(
    transaction_id: str,
    sale: SalesTransactionUpdate,
    db: Session = Depends(get_db)
):

    return update_sale(
        db,
        transaction_id,
        sale
    )


# ==================================================
# Delete Sale
# ==================================================

@router.delete("/{transaction_id}")
def remove_sale(
    transaction_id: str,
    db: Session = Depends(get_db)
):

    return delete_sale(
        db,
        transaction_id
    )
