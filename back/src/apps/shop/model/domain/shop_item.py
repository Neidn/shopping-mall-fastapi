from typing import Optional

import datetime
from pydantic import BaseModel
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, DateTime

from .....core.database import Base


class ShopItem(BaseModel):
    """ Shop Item """

    id: str
    name: str
    description: str
    price: int
    owner_id: str
    disabled: bool = False
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attribute = True
        orm_mode = True


class ShopItemDB(Base):
    __tablename__ = "shop_item"

    id = Column(
        String,
        primary_key=True,
        index=True,
        comment="Item id",
    )
    name = Column(
        String,
        index=True,
        default="",
        server_default="",
        comment="Item name",
    )
    description = Column(
        String,
        index=True,
        default="",
        server_default="",
        comment="Item description",
    )
    price = Column(
        Integer,
        index=True,
        default=0,
        server_default="0",
        comment="Item price",
    )
    owner_id = Column(
        String,
        ForeignKey("users.id"),
        index=True,
        default=0,
        server_default="0",
        comment="Owner id",
    )
    disabled = Column(
        Boolean,
        index=True,
        default=False,
        server_default="false",
        comment="Disabled",
    )
    created_at = Column(
        DateTime,
        index=True,
        comment="Created time",
    )
    updated_at = Column(
        DateTime,
        index=True,
        comment="Updated time",
    )
