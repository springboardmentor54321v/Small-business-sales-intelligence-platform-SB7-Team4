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

    model_config = ConfigDict(from_attributes=True)
