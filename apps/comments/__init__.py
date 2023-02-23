from fastapi import APIRouter


from apps.comments.views import comment_router

comment_routers = APIRouter()
comment_routers.include_router(comment_router)