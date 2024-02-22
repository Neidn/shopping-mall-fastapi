"""
Shop Router
"""
from typing import List, Dict, Optional
from starlette import status
from fastapi.routing import APIRouter
from fastapi.param_functions import Depends, Path, Security

from sqlalchemy.orm import Session

from ..apps.shop.model.schema.shop_item import ShopItemResponse, ShopItemCreateRequest, ShopItemCountResponse, \
    ShopItemUpdateRequest
from ..apps.auth.service.user import get_current_active_user, get_current_user
from ..core.database import get_database_session
from ..apps.auth.constants import SupportScopes
from ..apps.auth.model.domain.user import User
from ..apps.shop.service import shop as services
from ..core.config import settings
from .. import check_uuid

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


@shop_router.get(
    "/",
    response_model=List[ShopItemResponse],
    status_code=status.HTTP_200_OK
)
async def get_shop_items(
        db: Session = Depends(get_database_session),
        current_user: User = __readable_user,
        limit: int = settings.shop_item_default_limit,
        page: int = settings.shop_item_default_page,
) -> List[ShopItemResponse]:
    """
    Get all ShopItems
    """

    shop_items = services.get_all(
        db=db,
        owner_id=current_user.id,
        limit=limit,
        page=page,
    )
    response = [ShopItemResponse.from_orm(shop_item) for shop_item in shop_items]
    return response


@shop_router.get(
    '/{shop_item_id}',
    response_model=ShopItemResponse,
    status_code=status.HTTP_200_OK
)
async def get_shop_item(
        shop_item_id: str = __valid_id,
        db: Session = Depends(get_database_session),
        current_user: User = __readable_user,
) -> ShopItemResponse:
    """
    Get a ShopItem by ID
    """
    check = check_uuid(shop_item_id)
    if not check:
        raise ValueError(f"ShopItem with ID {shop_item_id} not found")

    shop_item = services.get_one(
        db=db,
        shop_item_id=shop_item_id,
        owner_id=current_user.id,
    )
    return ShopItemResponse.from_orm(shop_item)


@shop_router.get(
    '/count',
    response_model=ShopItemCountResponse,
    status_code=status.HTTP_200_OK
)
async def count_shop_items(
        db: Session = Depends(get_database_session),
        current_user: User = __readable_user,
) -> ShopItemCountResponse:
    """
    Count all ShopItems and pages
    """
    count, pages = services.count(
        db=db,
        owner_id=current_user.id,
    )
    return ShopItemCountResponse(
        count=count,
    )


@shop_router.patch(
    '/{shop_item_id}',
    response_model=ShopItemResponse,
    status_code=status.HTTP_200_OK
)
async def update_shop_item(
        update_request: ShopItemUpdateRequest,
        db: Session = Depends(get_database_session),
        shop_item_id: str = __valid_id,
        current_user: User = __updatable_user,
) -> ShopItemResponse:
    """
    Update a ShopItem by ID
    """
    check = check_uuid(shop_item_id)
    if not check:
        raise ValueError(f"ShopItem with ID {shop_item_id} not found")

    shop_item_check = services.get_one(
        db=db,
        shop_item_id=shop_item_id,
        owner_id=current_user.id,
    )

    if shop_item_check.disabled:
        raise ValueError(f"ShopItem with ID {shop_item_id} is disabled")

    shop_item = services.update_one(
        db=db,
        shop_item_id=shop_item_id,
        owner_id=current_user.id,
        update_request=update_request,
    )
    return ShopItemResponse.from_orm(shop_item)
