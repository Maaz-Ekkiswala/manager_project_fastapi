from fastapi import APIRouter


from apps.projects.views import project_router

projects_router = APIRouter()
projects_router.include_router(project_router)