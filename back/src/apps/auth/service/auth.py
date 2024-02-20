import time
from typing import Iterable, List, Optional

from fastapi.param_functions import Depends, Security
from sqlalchemy.orm import Session

from passlib.context import CryptContext

from ....core.database import get_database_session
from ..model.domain.user import User, UserDB
from ..constants import UserPermission
from ..exceptions import *
from . import verify_password
from .user import get_user
from .token import create_access_token


async def authenticate_user(
        db: Session,
        email: str,
        password: str,
) -> User:
    user: Optional[User] = await get_user(
        db=db,
        email=email
    )

    if user is None:
        raise ValueError("User not found")

    if not verify_password(password, user.hashed_password):
        raise ValueError("Invalid password")

    return user
