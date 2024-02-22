# pylint: disable=no-self-argument
"""
Shop Item Schema
"""
from typing import Dict, Optional

from pydantic import field_validator, ValidationInfo, BaseModel
from fastapi.exceptions import HTTPException


class ShopItemCreateRequest(BaseModel):
    """ Create a new shop item """
    name: str
    description: str
    price: int
    disabled: bool = False

    # @validator("repeat_plain_password")
    @field_validator("price")
    def price_validator(  # type: ignore
            cls,
            v: int,
            **kwargs  # noqa
    ) -> int:
        """ price validator """
        if v < 0:
            raise HTTPException(
                status_code=400,
                detail="price must be greater than or equal to 0",
            )
        return v

    class Config:
        from_attributes = True


class ShopItemResponse(BaseModel):
    """ Shop Item Response """
    id: str
    name: str
    description: str
    price: int
    owner_id: str
    disabled: bool

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "12345678-123",
                "name": "Item Name",
                "description": "Item Description",
                "price": 100,
                "owner_id": "123456",
                "disabled": False,
            }
        }


class ShopItemCountResponse(BaseModel):
    """ Shop Item Count Response """
    count: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "count": 10,
            }
        }


class ShopItemUpdateRequest(BaseModel):
    """ Update a shop item """
    name: str | None = None
    description: str | None = None
    price: int | None = None
    disabled: bool | None = None

    @field_validator("price")
    def price_validator(  # type: ignore
            cls,
            v: int,
            **kwargs  # noqa
    ) -> int:
        """ price validator """
        # if price is None or price < 0:
        # return None
        if v is None:
            return None

        if v is not None and v < 0:
            raise HTTPException(
                status_code=400,
                detail="price must be greater than or equal to 0",
            )

        return v

    class Config:
        from_attributes = True
