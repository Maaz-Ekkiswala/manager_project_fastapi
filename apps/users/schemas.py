from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreateUser(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: str
    password_hash: str
    is_superuser: Optional[bool]
    mobile: str


class UpdateUser(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    mobile: Optional[str]


class UserSchema(BaseModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    username: str
    is_active: bool
    is_superuser: Optional[bool]
    mobile: str
    created_at: datetime
    modified_at: datetime


class LoginSchema(BaseModel):
    username: str
    password_hash: str


class GetAuthSchema(BaseModel):
    access: str
    refresh: str
    user: UserSchema
