from fastapi import HTTPException
from starlette import status
from tortoise import fields
from tortoise.models import Model

from apps.master.models import Category
from core.base import Base


class Project(Model, Base):
    category = fields.ForeignKeyField(
        model_name="models.Category", related_name="project_category", on_delete='CASCADE'
    )
    name = fields.CharField(max_length=100, unique=True)
    description = fields.TextField(null=True, required=False)
    url = fields.CharField(max_length=100)
    category_data: fields.ForeignKeyRelation[Category]

    @classmethod
    async def get_project_by_id(cls, project_id):
        existing_project = await cls.get_or_none(id=project_id)
        if not existing_project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project not Found"
            )
        if not existing_project.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Project is inactive"
            )
        return existing_project


class ProjectUser(Model, Base):
    project = fields.ForeignKeyField(
        model_name="models.Project", related_name="project_id", on_delete='CASCADE'
    )
    user = fields.ForeignKeyField(
        model_name="models.User", related_name="project_users", on_delete='CASCADE'
    )