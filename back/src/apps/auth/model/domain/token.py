from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, String, ForeignKey, DateTime

from ...constants import TokenType
from .....core.database import Base


class TokenData(BaseModel):
    """ Token Data """
    user_id: str
    token_type: TokenType = TokenType.BEARER
    scopes: list[str] = []
    created_at: int
    expire_at: int

    class Config:
        from_attribute = True
