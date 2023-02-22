from tortoise import fields
from tortoise.models import Model

from core.base import Base


class Comment(Model, Base):
    issue = fields.ForeignKeyField(
        model_name="models.Issue", related_name="comment_issue", on_delete='CASCADE'
    )
    commented_by = fields.ForeignKeyField(
        model_name="models.User", related_name="commented_by", on_delete='CASCADE'
    )
    description = fields.TextField()
