import logging
from typing import List

from fastapi import APIRouter, Depends

from apps.issues.models import Issue
from apps.issues.schemas import IssueSchema, CreateIssue, UpdateIssue, UpdatePutIssue
from apps.projects.models import Project
from apps.projects.schemas import ProjectIssuesSchema
from core.valid_user import valid_user

issue_router = APIRouter(tags=["issue"])

logger = logging.getLogger(__name__)


@issue_router.post("/project/{id}/", response_model=IssueSchema)
async def create_issue(
        id: int,
        payload: CreateIssue,
        user: dict = Depends(valid_user)
):
    logger.debug(f"Trying to create issue by user {user.get('id')}")
    issue_instance = await Issue.create_issue(
        **payload.dict(exclude_unset=True), project_id=id
    )
    return issue_instance


@issue_router.get("/project/{id}/issues", response_model=ProjectIssuesSchema)
async def get_project_issues(
        id: int,
        user: dict = Depends(valid_user)
):
    logger.debug(f"Trying to fetch issues for project {id} by user {user.get('id')}")
    issues = await Issue.filter(project_id=id)
    return issues


@issue_router.get("/project/{id}/issue/{issue_id}/", response_model=IssueSchema)
async def get_issue_by_id(
        id: int,
        issue_id: int,
        user: dict = Depends(valid_user)
):
    logger.debug(
        f"Trying to get issue '{issue_id}' of project '{id}' by user {user.get('id')}"
    )
    issue_instance = await Issue.get_issue_by_id_with_project_id(project_id=id, issue_id=issue_id)
    return issue_instance


@issue_router.put("/project/{id}/issue/{issue_id}/", response_model=IssueSchema)
async def update_issue(
        payload: UpdatePutIssue,
        id: int,
        issue_id: int,
        user: dict = Depends(valid_user)
):
    logger.debug(
        f"Trying to update issue '{issue_id}' of project '{id}' by user {user.get('id')}"
    )
    issue_instance = await Issue.get_issue_by_id_with_project_id(project_id=id, issue_id=issue_id)
    updated_instance = await issue_instance.update_from_dict(data=payload.dict())
    return updated_instance


@issue_router.patch("/project/{id}/issue/{issue_id}/", response_model=IssueSchema)
async def update_issue(
        payload: UpdateIssue,
        id: int,
        issue_id: int,
        user: dict = Depends(valid_user)
):
    logger.debug(
        f"Trying to update issue '{issue_id}' of project '{id}' by user {user.get('id')}"
    )
    issue_instance = await Issue.get_issue_by_id_with_project_id(project_id=id, issue_id=issue_id)
    updated_instance = await issue_instance.update_from_dict(
        data=payload.dict(exclude_unset=True)
    )
    return updated_instance


