from typing import List
from .constants import UserPermission, SupportScopes


def user_permission_to_scopes(user_permission: UserPermission) -> List[str]:
    if user_permission == UserPermission.GUEST:
        return [
            SupportScopes.SHOP_USER_READ,
            SupportScopes.SHOP_PRODUCT_READ,
        ]
    elif user_permission == UserPermission.NORMAL:
        return [
            SupportScopes.SHOP_USER_READ,
            SupportScopes.SHOP_USER_WRITE,
            SupportScopes.SHOP_USER_DELETE,
            SupportScopes.SHOP_USER_UPDATE,
            SupportScopes.SHOP_PRODUCT_READ,
            SupportScopes.SHOP_PRODUCT_WRITE,
            SupportScopes.SHOP_PRODUCT_DELETE,
            SupportScopes.SHOP_PRODUCT_UPDATE,
            SupportScopes.SHOP_ORDER_READ,
            SupportScopes.SHOP_ORDER_WRITE,
            SupportScopes.SHOP_ORDER_DELETE,
            SupportScopes.SHOP_ORDER_UPDATE,
        ]
    elif user_permission == UserPermission.ADMIN:
        return [scope.value for scope in SupportScopes]
    else:
        return []
