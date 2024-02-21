from typing import List
from sqlalchemy.orm import Session
from datetime import datetime

from .... import get_new_id
from ..model.domain.shop_item import ShopItem, ShopItemDB
from ..model.schema.shop_item import ShopItemCreateRequest


def get_all(
        db: Session,
        owner_id: str
) -> List[ShopItem]:
    shop_items = db.query(ShopItemDB).filter_by(owner_id=owner_id).all()

    shop_items = [ShopItem.from_orm(shop_item) for shop_item in shop_items]
    return shop_items


def create_one(
        db: Session,
        shop_item: ShopItemCreateRequest,
        owner_id: str
) -> ShopItem:
    new_shop_item = ShopItemDB(
        id=get_new_id(),
        name=shop_item.name,
        description=shop_item.description,
        price=shop_item.price,
        owner_id=owner_id,
        disabled=shop_item.disabled,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    db.add(new_shop_item)
    db.commit()
    db.refresh(new_shop_item)
    return ShopItem(
        id=new_shop_item.id,
        name=new_shop_item.name,
        description=new_shop_item.description,
        price=new_shop_item.price,
        owner_id=new_shop_item.owner_id,
        disabled=new_shop_item.disabled,
        created_at=new_shop_item.created_at,
        updated_at=new_shop_item.updated_at,
    )
