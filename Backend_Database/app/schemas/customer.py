from typing import Optional

from pydantic import BaseModel, ConfigDict


class CustomerBase(BaseModel):
    customer_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class CustomerResponse(CustomerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
