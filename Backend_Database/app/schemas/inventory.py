from pydantic import BaseModel, ConfigDict


class InventoryBase(BaseModel):
    product_id: str
    stock_quantity: int
    low_stock_threshold: int


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    stock_quantity: int
    low_stock_threshold: int


class InventoryResponse(InventoryBase):
    id: int
    product_name: str
    category: str

    model_config = ConfigDict(from_attributes=True)

# =====================================================
# Bulk Update Schemas
# =====================================================

class InventoryBulkUpdateItem(BaseModel):
    product_id: str
    stock_quantity: int


class InventoryBulkUpdateRequest(BaseModel):
    updates: list[InventoryBulkUpdateItem]


class InventoryBulkUpdateResponse(BaseModel):
    updated_count: int
    message: str
