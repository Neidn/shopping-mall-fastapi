import time
from typing import Iterable, List, Optional
from uuid import uuid4
from datetime import datetime

# import jwt
from fastapi.param_functions import Depends, Security, Annotated
from fastapi.security.oauth2 import SecurityScopes

from sqlalchemy.orm import Session

from ....core.database import get_database_session
from ..model.domain.user import User, UserDB
from ..constants import UserPermission, SupportScopes, Oauth2Scheme
from ..exceptions import token_credential_exception, InactiveUserException, ForbiddenException
from .token import decode_token
from . import is_enough_permissions, check_admin_user, create_hashed_password


def get_new_id() -> str:
    return str(uuid4())


async def create_user(
        username: str,
        email: str,
        full_name: str,
        plain_password: str,
        db: Session = Depends(get_database_session),
) -> User:
    # Create User
    hashed_password = create_hashed_password(plain_password)

    if not hashed_password:
        raise ValueError("Password is required")

    new_user = User(
        id=get_new_id(),
        username=username,
        email=email,
        full_name=full_name,
        hashed_password=hashed_password,
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    # check if user exists
    user = db.query(UserDB).filter_by(email=email).first()
    if user:
        raise ValueError("User already exists")

    new_user_db = UserDB(**new_user.dict())
    db.add(new_user_db)
    db.commit()
    db.refresh(new_user_db)

    return new_user


async def get_current_user(
        security_scopes: SecurityScopes,
        token: Annotated[str, Depends(Oauth2Scheme)],
        db: Session = Depends(get_database_session),
) -> User:
    print('security_scopes', security_scopes.scopes)

    if security_scopes.scopes is None:
        raise ValueError("Security Scopes is required")

    # Check Current User
    credentials_exception = token_credential_exception(security_scopes.scope_str)

    token = await decode_token(token)

    print('token', token)
    print('token scopes', token.scopes)

    if token is None:
        raise credentials_exception

    if token.expire_at < time.time():
        raise credentials_exception

    user = db.query(UserDB).filter_by(id=token.user_id).first()

    if user is None:
        raise credentials_exception

    user = User(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=user.hashed_password,
        disabled=user.disabled,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )

    if not is_enough_permissions(token.scopes, security_scopes.scopes):
        credentials_exception.detail = "Insufficient permissions"
        raise credentials_exception

    return user


async def get_admin_user(
        current_user: User = Security(get_current_user)
) -> User:
    if not check_admin_user(current_user):
        raise ForbiddenException
    return current_user


async def get_current_active_user(
        current_user: User = Security(get_current_user),
) -> User:
    # Check Current Active User
    if current_user.disabled:
        raise InactiveUserException

    return current_user


async def get_user(
        email: str,
        db: Session = Depends(get_database_session),
) -> Optional[User]:
    # Get User
    user = db.query(UserDB).filter_by(email=email).first()

    user = User(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=user.hashed_password,
        disabled=user.disabled,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )

    return user
