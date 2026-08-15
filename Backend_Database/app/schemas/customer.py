from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
)


class CustomerBase(BaseModel):

    customer_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None

    # =====================================================
    # Customer ID Validation
    # =====================================================

    @field_validator("customer_id")
    @classmethod
    def validate_customer_id(cls, value: str):

        value = value.strip()

        if not value:
            raise ValueError(
                "Customer ID cannot be empty."
            )

        return value

    # =====================================================
    # Name Validation
    # =====================================================

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):

        value = value.strip()

        if not value:
            raise ValueError(
                "Customer name cannot be empty."
            )

        return value

    # =====================================================
    # Email Validation
    # =====================================================

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: Optional[str]):

        if value is None:
            return None

        value = value.strip()

        if not value:
            raise ValueError(
                "Email cannot be empty."
            )

        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError(
                "Invalid email format."
            )

        return value

    # =====================================================
    # Phone Validation
    # =====================================================

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: Optional[str]):

        if value is None:
            return None

        value = value.strip()

        if not value:
            raise ValueError(
                "Phone cannot be empty."
            )

        return value


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):

    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class CustomerResponse(CustomerBase):

    id: int

    model_config = ConfigDict(
        from_attributes=True
    )
