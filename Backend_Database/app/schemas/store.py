from typing import Optional

from pydantic import BaseModel, ConfigDict


class StoreBase(BaseModel):
    store_id: str
    store_name: str
    location: Optional[str] = None


class StoreCreate(StoreBase):
    pass


class StoreUpdate(BaseModel):
    store_name: Optional[str] = None
    location: Optional[str] = None


class StoreResponse(StoreBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
