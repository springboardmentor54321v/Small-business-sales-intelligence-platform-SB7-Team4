from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerResponse

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)

@router.get("/", response_model=list[CustomerResponse])
def get_customers(
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * page_size
    customers = db.query(Customer).offset(offset).limit(page_size).all()
    return customers

@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    req: CustomerCreate,
    db: Session = Depends(get_db)
):
    # Check if duplicate exists
    existing = db.query(Customer).filter(Customer.customer_id == req.customer_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Customer ID '{req.customer_id}' already exists."
        )
    
    # Check if duplicate email exists
    if req.email:
        existing_email = db.query(Customer).filter(Customer.email == req.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email '{req.email}' is already registered."
            )
            
    db_customer = Customer(
        customer_id=req.customer_id,
        name=req.name,
        email=req.email,
        phone=req.phone
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.delete("/{customer_id}")
def delete_customer(
    customer_id: str,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found."
        )
    db.delete(customer)
    db.commit()
    return {"message": "Customer deleted successfully"}
