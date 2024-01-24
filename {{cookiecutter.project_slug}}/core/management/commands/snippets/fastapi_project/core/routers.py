from authentication.routers import router as router_users
from fastapi import APIRouter, Response

from .config import settings
from .health_check import HealthCheck

router_core = APIRouter(prefix="/core", tags=["core"])


@router_core.get("/")
async def health_check():
    return Response(
        content=await HealthCheck.check(),
        media_type="application/json",
    )


api_router = APIRouter(prefix=settings.api_str)
api_router.include_router(router_core)
api_router.include_router(router_users, prefix="/authentication")
