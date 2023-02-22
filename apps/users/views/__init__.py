from fastapi import APIRouter

from apps.users.views.auth_views import auth_router
from apps.users.views.user_views import user_router

users_router = APIRouter()
users_router.include_router(auth_router)
users_router.include_router(user_router)