import json
import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from apps.issues.schemas import IssueSchema, UpdatePutIssue, UpdateIssue
from apps.master.models import Category
# from apps.issues.models import Issue
from apps.projects.models import Project, ProjectUser
from apps.projects.schemas import (
    ProjectSchema, CreateProject, UpdateProjectSchema, UpdatePutProjectSchema,
    ProjectIssuesSchema, ProjectDetailedSchema, CreateProjectUser
)
from apps.users.models import User
from core.permissions import permissions
# from core.permissions import permissions
from core.valid_user import valid_user

project_router = APIRouter(prefix="/project", tags=["project"])

logger = logging.getLogger(__name__)


@project_router.post("/", response_model=ProjectSchema)
async def create_project(
        payload: CreateProject,
        user: dict = Depends(valid_user)
):
    await Project.is_name_exist(name=payload.name)
    logger.debug(f"Trying to create project by user {user.get('id')}")
    project_instance = await Project.create(**payload.dict(exclude_unset=True))
    project_response = await Project.get_project_by_id_for_response(project_id=project_instance.id)
    return project_response


@project_router.get("/{id}", response_model=ProjectSchema)
@permissions(["project_user"])
async def get_project_by_id(
        id: int,
        user: dict = Depends(valid_user)
):
    logger.debug(f"Trying to fetch project {id} by user {user.get('id')}")
    project_instance = await Project.get_project_by_id_for_response(project_id=id)
    logger.debug(f"Project retrieved successfully {project_instance}")
    return project_instance.__dict__


@project_router.get("", response_model=List[ProjectSchema])
@permissions(["project_user"])
async def get_list_of_projects(user: dict = Depends(valid_user)):
    logger.debug(f"Trying to retrieve list of projects by user {user.get('id')}")
    project_instances = await Project.filter(is_active=True)
    project_response_list = []
    for project_instance in project_instances:
        project_dict = project_instance.__dict__
        project_dict['category'] = await Category.get(id=project_instance.category_id)
        project_dict['project_users'] = await ProjectUser.filter(
            project_id=project_instance.id
        ).values_list('user_id', flat=True)
        project_response_list.append(project_dict)
    return project_response_list


@project_router.put("/{id}/", response_model=ProjectSchema)
@permissions(["project_user"])
async def update_project(
        id: int,
        payload: UpdatePutProjectSchema,
        user: dict = Depends(valid_user)
):
    logger.debug(f"Trying to update project {id} by user {user.get('id')}")
    if payload.name:
        await Project.is_name_exist(payload.name)
    project_instance = await Project.get_project_by_id(project_id=id)
    await project_instance.update_from_dict(data=payload.dict())
    project_response = await Project.get_project_by_id_for_response(project_id=id)
    return project_response


@project_router.patch("/{id}/", response_model=ProjectSchema)
@permissions(["project_user"])
async def update_project(
        id: int,
        payload: UpdateProjectSchema,
        user: dict = Depends(valid_user)
):
    logger.debug(f"Trying to update project {id} by user {user.get('id')}")
    if payload.name:
        await Project.is_name_exist(payload.name)
    project_instance = await Project.get_project_by_id(project_id=id)
    await project_instance.update_from_dict(data=payload.dict(exclude_unset=True))
    project_response = await Project.get_project_by_id_for_response(project_id=id)
    return project_response


@project_router.post("/{id}/project-users/", response_model=ProjectSchema)
async def create_project_users(
        id: int,
        payload: CreateProjectUser,
        user: dict = Depends(valid_user)
):
    logger.debug(f"Trying to create project_users in project {id} by user {user.get('id')}")
    if not user.get('is_superuser'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to perform this action"
        )
    await User.get_multiple_user_by_ids(payload.users)
    project_instance = await Project.get_project_by_id(project_id=id)
    project_users_list = []
    await ProjectUser.filter(project=project_instance).delete()
    for project_user in payload.users:
        project_users_list.append(ProjectUser(project=project_instance, user_id=project_user))
    if project_users_list:
        await ProjectUser.bulk_create(project_users_list)
    project_user_response = await Project.get_project_by_id_for_response(project_id=id)
    return project_user_response

