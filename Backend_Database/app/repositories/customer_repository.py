from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.sales_transaction import SalesTransaction
from app.models.invoice import Invoice


# =====================================================
# Get All Customers
# =====================================================

def get_all_customers(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    search: str | None = None,
):

    query = db.query(Customer)

    # ==========================
    # Search
    # ==========================

    if search:
        search_pattern = f"%{search}%"

        query = query.filter(
            Customer.customer_id.ilike(search_pattern)
            | Customer.name.ilike(search_pattern)
            | Customer.email.ilike(search_pattern)
            | Customer.phone.ilike(search_pattern)
        )

    customers = (
        query
        .order_by(Customer.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return customers


# =====================================================
# Get Customer By ID
# =====================================================

def get_customer_by_id(
    db: Session,
    customer_id: str
):

    customer = (
        db.query(Customer)
        .filter(
            Customer.customer_id == customer_id
        )
        .first()
    )

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found."
        )

    return customer


# =====================================================
# Create Customer
# =====================================================

def create_customer(
    db: Session,
    customer
):

    existing_customer = (
        db.query(Customer)
        .filter(
            Customer.customer_id == customer.customer_id
        )
        .first()
    )

    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer ID already exists."
        )

    if customer.email:

        existing_email = (
            db.query(Customer)
            .filter(
                Customer.email == customer.email
            )
            .first()
        )

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer email already exists."
            )

    new_customer = Customer(
        customer_id=customer.customer_id,
        name=customer.name,
        email=customer.email,
        phone=customer.phone
    )

    db.add(new_customer)

    try:
        db.commit()
        db.refresh(new_customer)

    except Exception:
        db.rollback()
        raise

    return new_customer


# =====================================================
# Delete Customer
# =====================================================

def delete_customer(
    db: Session,
    customer_id: str,
):
    # ---------------------------------------------
    # Find customer
    # ---------------------------------------------
    customer = (
        db.query(Customer)
        .filter(
            Customer.customer_id == customer_id
        )
        .first()
    )

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found."
        )

    # ---------------------------------------------
    # Check sales transaction history
    # ---------------------------------------------
    has_sales = (
        db.query(SalesTransaction)
        .filter(
            SalesTransaction.customer_id == customer_id
        )
        .first()
    )

    if has_sales:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Customer cannot be deleted because "
                "sales transaction history exists."
            )
        )

    # ---------------------------------------------
    # Check invoice history
    # ---------------------------------------------
    has_invoices = (
        db.query(Invoice)
        .filter(
            Invoice.customer_id == customer_id
        )
        .first()
    )

    if has_invoices:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Customer cannot be deleted because "
                "invoice history exists."
            )
        )

    # ---------------------------------------------
    # Delete customer
    # ---------------------------------------------
    db.delete(customer)

    try:
        db.commit()

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Customer cannot be deleted because "
                "related records exist."
            )
        )

    return {
        "message": "Customer deleted successfully."
    }
