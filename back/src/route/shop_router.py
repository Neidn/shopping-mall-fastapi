"""
Health Check router
"""
from typing import Dict
from fastapi.routing import APIRouter

shop_router = APIRouter()


@shop_router.get("")
async def health_check() -> Dict[str, str]:
    """ health check """
    return {"status": "up"}
