from typing import List, Type
from sqlalchemy.orm import Session
from datetime import datetime

from .... import get_new_id
from ..model.domain.shop_item import ShopItem, ShopItemDB
from ..model.schema.shop_item import ShopItemCreateRequest, ShopItemUpdateRequest


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


def get_all(
        db: Session,
        owner_id: str,
        limit: int,
        page: int
) -> List[ShopItem]:
    shop_items_db: List[Type[ShopItemDB]] = db.query(ShopItemDB).filter_by(owner_id=owner_id).limit(limit).offset(
        (page - 1) * limit).all()

    shop_items: List[ShopItem] = [ShopItem.from_orm(shop_item) for shop_item in shop_items_db]
    return shop_items


def get_one(
        db: Session,
        shop_item_id: str,
        owner_id: str
) -> ShopItem:
    shop_item_db: Type[ShopItemDB] = db.query(ShopItemDB).filter_by(id=shop_item_id, owner_id=owner_id).first()

    if shop_item_db is None:
        raise ValueError(f"ShopItem with ID {shop_item_id} not found")

    return ShopItem.from_orm(shop_item_db)


def count(
        db: Session,
        owner_id: str,
) -> int:
    return db.query(ShopItemDB).filter_by(owner_id=owner_id).count()


def update_one(
        db: Session,
        shop_item_id: str,
        update_request: ShopItemUpdateRequest,
        owner_id: str
) -> ShopItem:
    shop_item_db = db.query(ShopItemDB).filter_by(id=shop_item_id, owner_id=owner_id).first()

    if shop_item_db is None:
        raise ValueError(f"ShopItem with ID {shop_item_id} not found")

    shop_item_db.name = update_request.name if update_request.name is not None else shop_item_db.name
    shop_item_db.description = update_request.description if update_request.description is not None else shop_item_db.description
    shop_item_db.price = update_request.price if update_request.price is not None else shop_item_db.price
    shop_item_db.disabled = update_request.disabled if update_request.disabled is not None else shop_item_db.disabled
    shop_item_db.updated_at = datetime.now()

    db.commit()
    db.refresh(shop_item_db)

    return ShopItem.from_orm(shop_item_db)



