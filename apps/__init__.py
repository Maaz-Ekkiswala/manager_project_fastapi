from fastapi import APIRouter

from apps.users.views import users_router

api_router = APIRouter()

api_router.include_router(users_router, prefix="/api/v1")