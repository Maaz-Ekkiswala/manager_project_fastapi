from fastapi import HTTPException
from starlette import status
from tortoise import fields
from tortoise.models import Model

from apps.issues.models import Issue
from core.base import Base


class Comment(Model, Base):
    issue = fields.ForeignKeyField(
        model_name="models.Issue", related_name="comment_issue", on_delete='CASCADE'
    )
    commented_by = fields.ForeignKeyField(
        model_name="models.User", related_name="commented_by", on_delete='CASCADE'
    )
    description = fields.TextField()

    @classmethod
    async def create_comment(cls, comment_data, issue_id):
        issue_instance = await Issue.get_issue_by_id(issue_id)
        comment_data['issue_id'] = issue_instance.id
        comment_instance = await cls.create(**comment_data)
        return comment_instance

    @classmethod
    async def get_comment_by_id_with_issue(
            cls, issue_id, comment_id, logged_in_user
    ):
        issue_instance = await Issue.get_issue_by_id(issue_id)
        comment_instance = await cls.get_or_none(
            id=comment_id, issue_id=issue_instance.id
        )
        if comment_instance.commented_by.id != logged_in_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"You cannot update or delete other's comment"
            )
        return comment_instance