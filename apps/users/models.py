from typing import Optional

from fastapi import HTTPException
from starlette import status
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model

from apps.users.functions import get_password_hash
from core.base import Timestamp


class User(Model, Timestamp):
    id = fields.IntField(pk=True, autoincrement=True)
    first_name = fields.CharField(max_length=255, null=True, required=False)
    last_name = fields.CharField(max_length=255, null=True, required=False)
    username = fields.CharField(max_length=100, unique=True)
    mobile = fields.CharField(max_length=10, unique=True)
    password_hash = fields.CharField(max_length=255)

    def __str__(self):
        return f"name: {self.first_name} {self.last_name}"

    class Meta:
        table: str = 'users'

    @classmethod
    async def create_user(
            cls,
            username: str,
            first_name: Optional[str],
            last_name: Optional[str],
            mobile: str,
            password_hash: str
    ) -> "User":
        hashed_password = str(get_password_hash(password_hash))
        user = await cls.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            password_hash=hashed_password
        )
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


User_Pydantic = pydantic_model_creator(User, name="User", exclude=("password_hash",))
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
UserUpdate_Pydantic = pydantic_model_creator(
    User, name="UserUpdate", exclude=(
        "password_hash", "username", "created_at", "modified_at", "id"
    )
)
UserLogin_Pydantic = pydantic_model_creator(
    User, name="UserLogin", include=("username", "password_hash")
)
