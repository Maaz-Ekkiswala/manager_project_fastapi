from fastapi import APIRouter

from apps.comments import comment_routers
from apps.issues import issues_router
from apps.master import master_router
from apps.projects import projects_router
from apps.users.views import users_router

api_router = APIRouter()

api_router.include_router(users_router, prefix="/api/v1")
api_router.include_router(master_router, prefix="/api/v1")
api_router.include_router(projects_router, prefix="/api/v1")
api_router.include_router(issues_router, prefix="/api/v1")
api_router.include_router(comment_routers, prefix="/api/v1")