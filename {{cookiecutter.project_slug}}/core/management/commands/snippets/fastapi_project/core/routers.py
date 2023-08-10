from authentication.routers import router as router_users
from fastapi import APIRouter

from .config import settings

api_router = APIRouter(prefix=settings.api_str)
api_router.include_router(router_users, prefix="/authentication")
