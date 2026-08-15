from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.customer import (
    CustomerCreate,
    CustomerResponse,
)

from app.repositories.customer_repository import (
    get_all_customers,
    create_customer,
    delete_customer,
)


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


# =====================================================
# Get All Customers
# =====================================================

@router.get(
    "/",
    response_model=list[CustomerResponse]
)
def get_customers(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    db: Session = Depends(get_db),
):

    return get_all_customers(
        db=db,
        page=page,
        page_size=page_size,
        search=search,
    )


# =====================================================
# Create Customer
# =====================================================

@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED
)
def add_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
):

    return create_customer(
        db=db,
        customer=customer,
    )


# =====================================================
# Delete Customer
# =====================================================

@router.delete(
    "/{customer_id}"
)
def remove_customer(
    customer_id: str,
    db: Session = Depends(get_db),
):

    return delete_customer(
        db=db,
        customer_id=customer_id,
    )
