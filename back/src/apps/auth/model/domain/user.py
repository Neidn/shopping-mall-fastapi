from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, DateTime

from ...constants import UserPermission
from .....core.database import Base


class User(BaseModel):
    """ User Info """

    id: str
    username: str
    email: str
    full_name: str
    hashed_password: str
    disabled: bool = False
    permission: UserPermission = UserPermission.NORMAL
    created_at: str
    updated_at: str

    class Config:
        from_attribute = True


class UserDB(Base):
    """ User DB """

    __tablename__ = "users"

    id = Column(
        String,
        primary_key=True,
        index=True,
        default="",
        server_default="",
        comment="User uuid",
    )
    username = Column(
        String,
        index=True,
        default="",
        server_default="",
        comment="User name",
    )
    email = Column(
        String,
        index=True,
        unique=True,
        default="",
        server_default="",
        comment="User email",
    )
    full_name = Column(
        String,
        index=True,
        default="",
        server_default="",
        comment="User full name",
    )
    hashed_password = Column(
        String,
        default="",
        server_default="",
        comment="User hashed password",
    )
    disabled = Column(
        Boolean,
        index=True,
        default=False,
        server_default="",
        comment="User disabled Status(True: disabled, False: enabled)",
    )
    permission = Column(
        Integer,
        index=True,
        default=UserPermission.NORMAL,
        server_default="",
        comment="User permission(GUEST: 0, NORMAL: 1, ADMIN: 2)",
    )
    created_at = Column(
        String,
        index=True,
        default="",
        server_default="",
        comment="User created at"
    )  # format: %Y-%m-%d %H:%M:%S
    updated_at = Column(
        String,
        index=True,
        default="",
        server_default="",
        comment="User updated at"
    )  # format: %Y-%m-%d %H:%M:%S
