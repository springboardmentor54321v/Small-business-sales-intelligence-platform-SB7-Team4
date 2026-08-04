from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.store import Store
from decimal import Decimal

from app.repositories.invoice_repository import (
    generate_invoice_number,
    create_invoice
)

from app.repositories.invoice_item_repository import (
    add_invoice_item
)

from app.repositories.invoice_repository import (
    bulk_update_invoices,
)

def validate_customer(
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

def validate_store(
    db: Session,
    store_id: str
):

    store = (
        db.query(Store)
        .filter(
            Store.store_id == store_id
        )
        .first()
    )

    if store is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found."
        )

    return store

def validate_product(
    db: Session,
    product_id: str
):

    product = (
        db.query(Product)
        .filter(
            Product.product_id == product_id
        )
        .first()
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )

    return product

def check_inventory(
    db: Session,
    product_id: str,
    quantity: int
):

    inventory = (
        db.query(Inventory)
        .filter(
            Inventory.product_id == product_id
        )
        .first()
    )

    if inventory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory record not found."
        )

    if inventory.stock_quantity < quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient stock available."
        )

    return inventory


def calculate_invoice_totals(
    db: Session,
    items
):

    subtotal = Decimal("0.00")
    discount_amount = Decimal("0.00")

    invoice_items = []

    for item in items:

        product = validate_product(
            db,
            item.product_id
        )

        check_inventory(
            db,
            item.product_id,
            item.quantity
        )

        unit_price = product.unit_price

        line_total = unit_price * item.quantity

        subtotal += line_total

        invoice_items.append({
            "product": product,
            "product_id": product.product_id,
            "product_name": product.product_name,
            "category": product.category,
            "quantity": item.quantity,
            "unit_price": unit_price,
            "line_total": line_total
        })

    tax_amount = subtotal * Decimal("0.18")

    total_amount = subtotal - discount_amount + tax_amount

    return {
        "subtotal": subtotal,
        "discount_amount": discount_amount,
        "tax_amount": tax_amount,
        "total_amount": total_amount,
        "invoice_items": invoice_items
    }

def create_invoice_service(
    db: Session,
    invoice
):
    validate_customer(
        db,
        invoice.customer_id
    )

    validate_store(
        db,
        invoice.store_id
    )

    invoice_totals = calculate_invoice_totals(
        db,
        invoice.items
    )

    invoice_number = generate_invoice_number(db)
    invoice_id = invoice_number

    invoice_data = {
        "invoice_id": invoice_id,
        "invoice_number": invoice_number,
        "customer_id": invoice.customer_id,
        "store_id": invoice.store_id,
        "created_by_user_id": invoice.created_by_user_id,
        "invoice_date": invoice.invoice_date,
        "due_date": invoice.due_date,
        "subtotal": invoice_totals["subtotal"],
        "discount_amount": invoice_totals["discount_amount"],
        "tax_amount": invoice_totals["tax_amount"],
        "total_amount": invoice_totals["total_amount"],
        "payment_status": "Pending",
        "invoice_status": "Generated",
        "notes": invoice.notes
    }

    invoice_record = create_invoice(
        db,
        invoice_data
    )

    for item in invoice_totals["invoice_items"]:
        item_data = {
        "invoice_id": invoice_id,
        "product_id": item["product_id"],
        "quantity": item["quantity"],
        "unit_price": item["unit_price"],
        "discount": Decimal("0.00"),
        "tax": Decimal("0.00"),
        "line_total": item["line_total"],
        "category_snapshot": item["category"],
        "product_name_snapshot": item["product_name"]
    }
        add_invoice_item(
            db,
            item_data
        )

        inventory = check_inventory(
            db,
            item["product_id"],
            item["quantity"]
        )
        
        inventory.stock_quantity -= item["quantity"]

    db.commit()
    return invoice_record

# =====================================================
# Bulk Update Invoice Service
# =====================================================

from app.schemas.invoice import (
    InvoiceBulkUpdateRequest,
    InvoiceBulkUpdateResponse,
)


def bulk_update_invoice_service(
    db: Session,
    request: InvoiceBulkUpdateRequest,
) -> InvoiceBulkUpdateResponse:

    result = bulk_update_invoices(
        db=db,
        invoice_ids=request.invoice_ids,
        payment_status=request.payment_status,
    )

    return InvoiceBulkUpdateResponse(**result)
