from typing import List, Type
from sqlalchemy.orm import Session
from datetime import datetime

from .... import get_new_id
from ..model.domain.shop_item import ShopItem, ShopItemDB
from ..model.schema.shop_item import ShopItemCreateRequest


def get_all(
        db: Session,
        owner_id: str
) -> List[ShopItem]:
    shop_items_db: List[Type[ShopItemDB]] = db.query(ShopItemDB).filter_by(owner_id=owner_id).all()

    shop_items: List[ShopItem] = [ShopItem.from_orm(shop_item) for shop_item in shop_items_db]
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
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    db.add(new_shop_item)
    db.commit()
    db.refresh(new_shop_item)
    return ShopItem.from_orm(new_shop_item)
