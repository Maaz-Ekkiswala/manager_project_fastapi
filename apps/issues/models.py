from tortoise import fields
from tortoise.models import Model

from apps.issues.constants import Type, Status, Priority
from core.base import Base


class Issue(Model, Base):
    project = fields.ForeignKeyField(
        model_name="models.Project", related_name="issue_project", on_delete='CASCADE'
    )
    title = fields.CharField(max_length=100, unique=True)
    type = fields.CharEnumField(enum_type=Type, default=Type.TASK.value, max_length=20)
    status = fields.CharEnumField(
        enum_type=Status, default=Status.PENDING.value, max_length=50
    )
    priority = fields.CharEnumField(
        enum_type=Priority, default=Priority.LOWEST.value, max_length=30
    )
    description = fields.TextField(null=True, required=False)


class IssueUser(Model, Base):
    issue = fields.ForeignKeyField(
        model_name="models.Issue", related_name="issue_id", on_delete='CASCADE'
    )
    user = fields.ForeignKeyField(
        model_name="models.User", related_name="issue_users", on_delete='CASCADE'
    )
