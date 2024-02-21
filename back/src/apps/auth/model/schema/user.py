# pylint: disable=no-self-argument
"""
User Schema
"""
from typing import Dict

from pydantic import field_validator, ValidationInfo, BaseModel
from fastapi.exceptions import HTTPException

from ...constants import TokenType

__all__ = ["UserCreateRequest", "UserCreatedResponse", "UserSignInResponse"]


class UserCreateRequest(BaseModel):
    """ Register a new account """
    username: str
    email: str
    full_name: str
    plain_password: str
    repeat_plain_password: str

    # @validator("repeat_plain_password")
    @field_validator("repeat_plain_password")
    def password_match(  # type: ignore
            cls,
            v: str,
            values: ValidationInfo,
            **kwargs  # noqa
    ) -> str:
        """ password match """
        v = v.strip()

        if not values.data.get("plain_password"):
            raise HTTPException(
                status_code=400,
                detail="password is required",
            )

        values.data["plain_password"] = values.data.get("plain_password").strip()

        if v != values.data.get("plain_password"):
            raise HTTPException(
                status_code=400,
                detail="passwords do not match",
            )
        return v

    class Config:
        from_attributes = True


class UserCreatedResponse(BaseModel):
    """ User Created Response """
    username: str
    email: str
    full_name: str
    created_at: str

    class Config:
        from_attributes = True


class UserSignInResponse(BaseModel):
    username: str
    email: str
    full_name: str
    access_token: str
    token_type: TokenType

    class Config:
        from_attributes = True
