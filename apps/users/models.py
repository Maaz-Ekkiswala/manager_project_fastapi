from typing import Optional

from fastapi import HTTPException
from starlette import status
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model

from apps.users.functions import get_password_hash
from core.base import Base


class User(Model, Base):
    first_name = fields.CharField(max_length=255, null=True, required=False)
    last_name = fields.CharField(max_length=255, null=True, required=False)
    username = fields.CharField(max_length=100, unique=True)
    mobile = fields.CharField(max_length=10, unique=True)
    password_hash = fields.CharField(max_length=255)
    is_superuser = fields.BooleanField(default=False)

    class Meta:
        table: str = 'users'

    @classmethod
    async def create_user(cls, userdata):
        userdata["password_hash"] = str(get_password_hash(userdata.pop("password_hash")))
        user = await cls.create(**userdata)
        return user

    @classmethod
    async def check_mobile_exist(cls, mobile):
        existing_user = await cls.get_or_none(mobile=mobile)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Mobile already exists"
            )
        return True

    @classmethod
    async def get_user_by_id(cls, user_id):
        existing_user = await cls.get_or_none(id=user_id)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User not Found"
            )
        return existing_user

    @classmethod
    async def get_user_by_username(cls, username):
        existing_user = await cls.get_or_none(username=username)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User not Found"
            )
        return existing_user

    @classmethod
    async def get_multiple_user_by_ids(cls, ids):
        users = await cls.filter(id__in=ids).values_list('id', flat=True)
        if not set(ids).issubset(set(users)):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User not Found"
            )
        return users

