import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from apps.projects.models import Project
from apps.projects.schemas import ProjectSchema, CreateProject
from core.valid_user import valid_user

project_router = APIRouter(prefix="/project", tags=["project"])

logger = logging.getLogger(__name__)


@project_router.post("/", response_model=ProjectSchema)
async def create_project(
        payload: CreateProject,
        user: dict = Depends(valid_user)
):
    if await Project.get_or_none(name=payload.name) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Project with {payload.name} already exists"
        )
    logger.debug(f"Trying to create project by user {user.get('id')}")
    project_instance = await Project.create(**payload.dict(exclude_unset=True))
    return project_instance


@project_router.get("/{id}", response_model=ProjectSchema)
async def get_project_by_id(
        id: int,
        user: dict = Depends(valid_user)
):
    logger.debug(f"Trying to fetch project {id} by user {user.get('id')}")
    # selected_events = await Project.filter(id=id).prefetch_related('project_category__category')
    # print(selected_events)
    project_instance = await Project.get_project_by_id(project_id=id)
    # print(project_instance.category.all())
    # x = await project_instance.fetch_related('category')
    # print(x)
    logger.debug(f"Project retrieved successfully {project_instance.__dict__}")
    return project_instance


@project_router.put("/{id}/", response_model=ProjectSchema)
async def update_project(
        id: int,
        user: dict = Depends(valid_user)
):
    logger.debug(f"Trying to update project {id} by user {user.get('id')}")
    pass
