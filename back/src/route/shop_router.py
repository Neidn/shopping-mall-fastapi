"""
Shop Router
"""
from typing import List, Dict
from starlette import status
from fastapi.routing import APIRouter
from fastapi.param_functions import Depends, Path, Security

from sqlalchemy.orm import Session

from ..apps.shop.model.schema.shop_item import ShopItemResponse, ShopItemCreateRequest
from ..apps.auth.service.user import get_current_active_user, get_current_user
from ..core.database import get_database_session
from ..apps.auth.constants import SupportScopes
from ..apps.auth.model.domain.user import User
from ..apps.shop.service import shop as services

shop_router = APIRouter()

# UUid
__valid_id = Path(
    ...,
    title="Shop Item ID",
    description="The ID of the ShopItem",
)

__current_active_user = Depends(get_current_active_user)
__creatable_user = Security(get_current_active_user, scopes=[SupportScopes.SHOP_PRODUCT_WRITE])
__readable_user = Security(get_current_active_user, scopes=[SupportScopes.SHOP_PRODUCT_READ])
__updatable_user = Security(get_current_active_user, scopes=[SupportScopes.SHOP_USER_UPDATE])
__deletable_user = Security(get_current_active_user, scopes=[SupportScopes.SHOP_USER_DELETE])


@shop_router.get(
    "/",
    response_model=List[ShopItemResponse],
    status_code=status.HTTP_200_OK
)
async def get_shop_items(
        db: Session = Depends(get_database_session),
        current_user: User = __readable_user,
) -> List[ShopItemResponse]:
    """
    Get all ShopItems
    """
    shop_items = services.get_all(
        db=db,
        owner_id=current_user.id,
    )
    response = [ShopItemResponse.from_orm(shop_item) for shop_item in shop_items]
    return response


@shop_router.post(
    "/",
    response_model=ShopItemCreateRequest,
    status_code=status.HTTP_201_CREATED
)
async def create_shop_item(
        shop_item: ShopItemCreateRequest,
        db: Session = Depends(get_database_session),
        current_user: User = __creatable_user,
) -> ShopItemResponse:
    """
    Create a new ShopItem
    """
    shop_item = services.create_one(
        db=db,
        shop_item=shop_item,
        owner_id=current_user.id,
    )

    return ShopItemResponse.from_orm(shop_item)
