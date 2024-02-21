from enum import Enum
from typing import List
from fastapi.security.oauth2 import OAuth2PasswordBearer

SPLITER = ","

class UserPermission(str, Enum):
    GUEST = 0
    NORMAL = 1
    ADMIN = 2


class TokenType(str, Enum):
    BEARER: str = "Bearer"


class SupportScopes(str, Enum):
    SHOP_USER_READ = "user:read:own"
    SHOP_USER_WRITE = "user:write:own"
    SHOP_USER_DELETE = "user:delete:own"
    SHOP_USER_UPDATE = "user:update:own"
    SHOP_USER_READ_ALL = "user:read:all"
    SHOP_USER_WRITE_ALL = "user:write:all"
    SHOP_USER_DELETE_ALL = "user:delete:all"
    SHOP_USER_UPDATE_ALL = "user:update:all"

    SHOP_PRODUCT_READ = "product:read:own"
    SHOP_PRODUCT_WRITE = "product:write:own"
    SHOP_PRODUCT_DELETE = "product:delete:own"
    SHOP_PRODUCT_UPDATE = "product:update:own"
    SHOP_PRODUCT_READ_ALL = "product:read:all"
    SHOP_PRODUCT_WRITE_ALL = "product:write:all"
    SHOP_PRODUCT_DELETE_ALL = "product:delete:all"
    SHOP_PRODUCT_UPDATE_ALL = "product:update:all"

    SHOP_ORDER_READ = "order:read:own"
    SHOP_ORDER_WRITE = "order:write:own"
    SHOP_ORDER_DELETE = "order:delete:own"
    SHOP_ORDER_UPDATE = "order:update:own"
    SHOP_ORDER_READ_ALL = "order:read:all"
    SHOP_ORDER_WRITE_ALL = "order:write:all"
    SHOP_ORDER_DELETE_ALL = "order:delete:all"
    SHOP_ORDER_UPDATE_ALL = "order:update:all"


Oauth2Scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={scope.name: scope.value for scope in SupportScopes}
)

