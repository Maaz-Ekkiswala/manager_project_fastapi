from datetime import datetime

from tortoise import fields


class Base:
    id = fields.IntField(pk=True, autoincrement=True)
    created_at: datetime = fields.DatetimeField(null=False, auto_now_add=True)
    modified_at: datetime = fields.DatetimeField(null=True, auto_now=True)
    is_active = fields.BooleanField(default=True)