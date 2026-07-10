from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.inventory import Inventory
from app.schemas.inventory import (
    InventoryCreate,
    InventoryUpdate,
    InventoryResponse,
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
def get_inventory(db: Session = Depends(get_db)):

    inventory = db.query(Inventory).all()

    return inventory


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
