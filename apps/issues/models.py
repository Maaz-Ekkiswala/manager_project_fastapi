from fastapi import HTTPException
from starlette import status
from tortoise import fields
from tortoise.models import Model

from apps.issues.constants import Type, Status, Priority
from apps.projects.models import Project
from core.base import Base


class Issue(Model, Base):
    project = fields.ForeignKeyField(
        model_name="models.Project", related_name="issue_project", on_delete='CASCADE'
    )
    title = fields.CharField(max_length=200)
    type = fields.CharEnumField(enum_type=Type, default=Type.TASK.value, max_length=20)
    status = fields.CharEnumField(
        enum_type=Status, default=Status.PENDING.value, max_length=50
    )
    priority = fields.CharEnumField(
        enum_type=Priority, default=Priority.LOWEST.value, max_length=30
    )
    description = fields.TextField(null=True, required=False)

    @classmethod
    async def create_issue(cls, issue_data, project_id):
        project_instance = await Project.get_project_by_id(project_id=project_id)
        issue_data['project_id'] = project_instance.id
        issue_instance = await cls.create(**issue_data)
        return issue_instance

    @classmethod
    async def get_issue_by_id_with_project_id(cls, project_id, issue_id):
        project_instance = await Project.get_project_by_id(project_id=project_id)
        existing_issue = await cls.get_or_none(
            project_id=project_instance.id, id=issue_id
        )
        if not existing_issue:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Issue not Found"
            )
        if not existing_issue.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Issue is inactive"
            )
        return existing_issue

    @classmethod
    async def get_issue_by_id(cls, issue_id):
        existing_issue = await cls.get_or_none(id=issue_id)
        if not existing_issue:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Issue not Found"
            )
        if not existing_issue.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Issue is inactive"
            )
        return existing_issue


class IssueUser(Model, Base):
    issue = fields.ForeignKeyField(
        model_name="models.Issue", related_name="issue_id", on_delete='CASCADE'
    )
    user = fields.ForeignKeyField(
        model_name="models.User", related_name="issue_users", on_delete='CASCADE'
    )

    class Meta:
        unique_together = ("issue", "user")