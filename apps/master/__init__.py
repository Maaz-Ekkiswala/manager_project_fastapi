from fastapi import APIRouter


from apps.master.views import category_router

master_router = APIRouter()
master_router.include_router(category_router)
