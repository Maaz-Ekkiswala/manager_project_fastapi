from typing import List

from fastapi import APIRouter, Depends

from apps.master.models import Category
from apps.master.schemas import CategorySchema
from core.valid_user import valid_user

category_router = APIRouter(prefix="/category", tags=["category"])


@category_router.get("", response_model=List[CategorySchema])
async def get_list_categories(user: dict = Depends(valid_user)):
    categories = await Category.all()
    return categories
