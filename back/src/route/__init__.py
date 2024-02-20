"""
routes
"""
from fastapi.routing import APIRouter

from .health_router import health_router

# from .todo_router import todos_router
from .user_router import user_router
from .shop_router import shop_router

__all__ = ["api_router", "health_router", "user_router", "shop_router"]

api_router = APIRouter()

api_router.include_router(health_router, prefix="/health", tags=["manage"])
api_router.include_router(user_router, prefix="/user", tags=["auth"])
api_router.include_router(shop_router, prefix="/shop", tags=["shop"])
