from fastapi import APIRouter

from .routes import test, auth

api_router = APIRouter()
api_router.include_router(test.router, prefix="/test", tags=["users"])
api_router.include_router(auth.auth_router, prefix="/auth", tags=["users"])
