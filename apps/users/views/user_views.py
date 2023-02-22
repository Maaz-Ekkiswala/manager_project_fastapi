import logging
from typing import List

from fastapi import APIRouter, Depends

from apps.users.models import User
from apps.users.schemas import UserSchema, UpdateUser
from core.valid_user import valid_user

user_router = APIRouter(prefix="/user", tags=["user"])

logger = logging.getLogger(__name__)


@user_router.get("/logged-in-user", response_model=UserSchema)
async def get_user(
        user: dict = Depends(valid_user)
):
    logger.debug(f"Trying to retrieve logged in user {user.get('id')}")
    user_instance = await User.get_user_by_id(user_id=user.get("id"))
    return user_instance


@user_router.get("/{id}", response_model=UserSchema)
async def get_user(
        id: int,
        user: dict = Depends(valid_user)
):
    logger.debug(f"Trying to retrieve user {id} by id")
    user_instance = await User.get_user_by_id(user_id=id)
    logger.debug(f"User retrieved successfully {user_instance.__dict__}")
    return user_instance


@user_router.get("", response_model=List[UserSchema])
async def get_list_user(user: dict = Depends(valid_user)):
    logger.debug(f"Trying to retrieve list of users  by {user.get('id')}")
    user_instances = await User.filter(is_active=True)
    logger.debug(f"List of users fetched {len(user_instances)}")
    return user_instances


@user_router.put("/{id}/", response_model=UserSchema)
async def update_user(
        id: int,
        payload: UpdateUser,
        user: dict = Depends(valid_user)
):
    logger.debug(f"Trying to update user {id} by user {user.get('id')}")
    user_instance = await User.get_user_by_id(user_id=id)
    if payload.mobile:
        await User.check_mobile_exist(mobile=payload.mobile)
    await User.filter(id=id).update(
        **payload.dict(exclude_unset=True)
    )
    logger.debug(f"User updated successfully {user_instance.__dict__}")
    return user_instance
