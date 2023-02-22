from tortoise import Model, fields
from tortoise.fields import ReverseRelation

from core.base import Base


class Category(Model, Base):
    name = fields.CharField(max_length=100, unique=True)
    description = fields.TextField(null=True, required=False)
