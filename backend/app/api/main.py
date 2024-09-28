from fastapi import APIRouter

from .routes.test import router
from .routes.auth import auth_router
from .routes.user import users_routers

api_router = APIRouter()
api_router.include_router(router, prefix="/api/test")
api_router.include_router(auth_router, prefix="/api")
api_router.include_router(users_routers, prefix="/api/users")
