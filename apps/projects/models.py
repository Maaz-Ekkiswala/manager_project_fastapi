from fastapi import HTTPException
from starlette import status
from tortoise import fields
from tortoise.models import Model

from apps.master.models import Category
from core.base import Base


class Project(Model, Base):
    category: fields.ForeignKeyRelation[Category] = fields.ForeignKeyField(
        model_name="models.Category", related_name="project_category", on_delete='CASCADE'
    )
    name = fields.CharField(max_length=100, unique=True)
    description = fields.TextField(null=True, required=False)
    url = fields.CharField(max_length=100)

    @classmethod
    async def is_name_exist(cls, name):
        is_name_exist = await cls.get_or_none(name=name)
        if is_name_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project with this name already exist"
            )
        return True

    @classmethod
    async def get_project_by_id_for_response(cls, project_id):
        existing_project = await cls.filter(id=project_id).first().prefetch_related('category')
        return existing_project
        # # project_dict = existing_project.__dict__
        # # project_dict['category'] = await Category.get(id=existing_project.category_id)
        # project_dict['project_users'] = await ProjectUser.filter(
        #     project_id=existing_project.id
        # ).values_list('user_id', flat=True)
        # if not existing_project:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail=f"Project not Found"
        #     )
        # if not existing_project.is_active:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail=f"Project is inactive"
        #     )
        # return project_dict

    @classmethod
    async def get_project_by_id(cls, project_id):
        existing_project = await cls.filter(id=project_id).first()
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

    class Meta:
        unique_together = ("project", "user")

    @classmethod
    async def get_multiple_user_by_ids(cls, ids, project_id):
        project_user_ids = await cls.filter(
            project_id=project_id, user_id__in=ids
        ).values_list('id', flat=True)
        if not set(ids).issubset(set(project_user_ids)):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project users not Found"
            )
        return project_user_ids