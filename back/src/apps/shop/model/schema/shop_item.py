# pylint: disable=no-self-argument
"""
Shop Item Schema
"""
from typing import Dict

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
