from datetime import datetime

from tortoise import fields


class Timestamp:
    created_at: datetime = fields.DatetimeField(null=False, auto_now_add=True)
    modified_at: datetime = fields.DatetimeField(null=True, auto_now=True)