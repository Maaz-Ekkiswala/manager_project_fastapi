from fastapi import APIRouter


from apps.issues.views import issue_router

issues_router = APIRouter()
issues_router.include_router(issue_router)