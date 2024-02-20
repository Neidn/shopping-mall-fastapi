import jwt
from typing import Iterable

from passlib.context import CryptContext

from ..model.domain.user import User
from ..constants import UserPermission
from ....core.config import settings

# with open(settings.PUBLIC_KEY_PATH, "r") as f:
#    settings.PUBLIC_KEY = f.read()

# with open(settings.PRIVATE_KEY_PATH, "r") as f:
#    settings.PRIVATE_KEY = f.read()

__pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def is_enough_permissions(
        scopes: Iterable[str],
        required_scopes: Iterable[str]
) -> bool:
    """ permission check """
    scopes_set = set(scopes)
    required_set = set(required_scopes)
    return scopes_set.issuperset(required_set)


def check_admin_user(
        current_user: User
) -> bool:
    """ admin user check """
    return current_user.permission == UserPermission.ADMIN


def verify_password(input_password: str, hashed_password: str) -> bool:
    verify = False

    try:
        verify: bool = __pwd_context.verify(input_password, hashed_password)
    except (ValueError, RuntimeError) as err:
        print(err)
        verify = False
    finally:
        return verify


def create_hashed_password(password: str) -> str:
    return __pwd_context.hash(password)


def get_password_hash(password: str) -> str:
    return __pwd_context.hash(password)
