from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.inventory import Inventory
from app.models.product import Product

from app.schemas.inventory import (
    InventoryCreate,
    InventoryUpdate,
    InventoryResponse,
    InventoryBulkUpdateRequest,
    InventoryBulkUpdateResponse,
)

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)


# ==================================================
# Get All Inventory
# ==================================================

@router.get(
    "/",
    response_model=list[InventoryResponse]
)
def get_inventory(

    page: int = Query(1, ge=1),

    page_size: int = Query(10, ge=1, le=100),

    category: str | None = Query(None),

    search: str | None = Query(None),

    db: Session = Depends(get_db),

):

    query = (
        db.query(Inventory)
        .join(Product)
    )

    # ==========================
    # Category Filter
    # ==========================

    if category:

        query = query.filter(
            Product.category.ilike(f"%{category}%")
        )

    # ==========================
    # Search
    # ==========================

    if search:

        query = query.filter(

            or_(

                Product.product_id.ilike(f"%{search}%"),

                Product.product_name.ilike(f"%{search}%"),

            )

        )

        query = query.order_by(Inventory.id)

    inventory = (
        query
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return inventory



# ==================================================
# Bulk Update Inventory
# ==================================================

@router.put(
    "/bulk-update",
    response_model=InventoryBulkUpdateResponse,
)
def bulk_update_inventory(
    request: InventoryBulkUpdateRequest,
    db: Session = Depends(get_db),
):

    if not request.updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No inventory updates provided."
        )

    updated_count = 0

    for item in request.updates:

        inventory = (
            db.query(Inventory)
            .filter(
                Inventory.product_id == item.product_id
            )
            .first()
        )

        if inventory is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f"Product {item.product_id} not found."
                )
            )

        inventory.stock_quantity = item.stock_quantity

        updated_count += 1

    try:
    # validation and update logic

        db.commit()

        return InventoryBulkUpdateResponse(
            updated_count=updated_count,
            message="Inventory updated successfully."
    )

    except Exception:
        db.rollback()
        raise

# ==================================================
# Get Inventory By Product ID
# ==================================================

@router.get(
    "/{product_id}",
    response_model=InventoryResponse
)
def get_inventory_item(
    product_id: str,
    db: Session = Depends(get_db)
):

    inventory = (
        db.query(Inventory)
        .filter(Inventory.product_id == product_id)
        .first()
    )

    if not inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory record not found."
        )

    return inventory


# ==================================================
# Add Inventory
# ==================================================

@router.post(
    "/",
    response_model=InventoryResponse,
    status_code=status.HTTP_201_CREATED
)
def add_inventory(
    inventory: InventoryCreate,
    db: Session = Depends(get_db)
):

    existing = (
        db.query(Inventory)
        .filter(
            Inventory.product_id == inventory.product_id
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Inventory already exists."
        )

    new_inventory = Inventory(**inventory.model_dump())

    db.add(new_inventory)
    db.commit()
    db.refresh(new_inventory)

    return new_inventory


# ==================================================
# Update Inventory
# ==================================================

@router.put(
    "/{product_id}",
    response_model=InventoryResponse
)
def update_inventory(
    product_id: str,
    updated_inventory: InventoryUpdate,
    db: Session = Depends(get_db)
):

    inventory = (
        db.query(Inventory)
        .filter(
            Inventory.product_id == product_id
        )
        .first()
    )

    if not inventory:
        raise HTTPException(
            status_code=404,
            detail="Inventory record not found."
        )

    inventory.stock_quantity = updated_inventory.stock_quantity
    inventory.low_stock_threshold = (
        updated_inventory.low_stock_threshold
    )

    db.commit()
    db.refresh(inventory)

    return inventory


# ==================================================
# Delete Inventory
# ==================================================

@router.delete("/{product_id}")
def delete_inventory(
    product_id: str,
    db: Session = Depends(get_db)
):

    inventory = (
        db.query(Inventory)
        .filter(
            Inventory.product_id == product_id
        )
        .first()
    )

    if not inventory:
        raise HTTPException(
            status_code=404,
            detail="Inventory record not found."
        )

    db.delete(inventory)
    db.commit()

    return {
        "message": "Inventory deleted successfully."
    }
