from enum import Enum
from fastapi.security.oauth2 import OAuth2PasswordBearer


class UserPermission(str, Enum):
    GUEST = 0
    NORMAL = 1
    ADMIN = 2


class TokenType(str, Enum):
    BEARER: str = "Bearer"


class SupportScopes(str, Enum):
    SHOP_USER_READ = "SHOP_USER_READ"
    SHOP_USER_WRITE = "SHOP_USER_WRITE"
    SHOP_USER_DELETE = "SHOP_USER_DELETE"
    SHOP_USER_UPDATE = "SHOP_USER_UPDATE"

    SHOP_PRODUCT_READ = "SHOP_PRODUCT_READ"
    SHOP_PRODUCT_WRITE = "SHOP_PRODUCT_WRITE"
    SHOP_PRODUCT_DELETE = "SHOP_PRODUCT_DELETE"
    SHOP_PRODUCT_UPDATE = "SHOP_PRODUCT_UPDATE"

    SHOP_PRODUCT_ALL_READ = "SHOP_PRODUCT_ALL_READ"
    SHOP_PRODUCT_ALL_WRITE = "SHOP_PRODUCT_ALL_WRITE"
    SHOP_PRODUCT_ALL_DELETE = "SHOP_PRODUCT_ALL_DELETE"
    SHOP_PRODUCT_ALL_UPDATE = "SHOP_PRODUCT_ALL_UPDATE"

    SHOP_ORDER_READ = "SHOP_ORDER_READ"
    SHOP_ORDER_WRITE = "SHOP_ORDER_WRITE"
    SHOP_ORDER_DELETE = "SHOP_ORDER_DELETE"
    SHOP_ORDER_UPDATE = "SHOP_ORDER_UPDATE"


Oauth2Scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={scope.name: scope.value for scope in SupportScopes}
)
