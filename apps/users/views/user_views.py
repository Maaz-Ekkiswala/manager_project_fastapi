import logging

from fastapi import APIRouter, Depends

from apps.users.models import UserUpdate_Pydantic, User, User_Pydantic
from core.valid_user import valid_user

user_router = APIRouter(prefix="/user", tags=["user"])

logger = logging.getLogger(__name__)


@user_router.get("")
async def get_user(
        user: dict =Depends(valid_user)
):
    user_instance = await User.get_user_by_id(user_id=user.get("id"))
    return await User_Pydantic.from_tortoise_orm(user_instance)


@user_router.put("/")
async def update_user(
        payload: UserUpdate_Pydantic,
        user: dict = Depends(valid_user)
):
    print(user)
    user_instance = await User.get_user_by_id(user_id=user.get("id"))

    updated_response = await User.filter(id=user.get("id")).update(**payload.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_instance)
