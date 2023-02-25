import logging

from fastapi import APIRouter, Depends
from starlette import status

from apps.issues.models import Issue, IssueUser
from apps.issues.schemas import (
    IssueSchema, CreateIssue, UpdateIssue, UpdatePutIssue, CreateIssueUser
)
from apps.projects.models import Project, ProjectUser
from apps.projects.schemas import ProjectIssuesSchema
from apps.users.models import User
from core.permissions import permissions
from core.valid_user import valid_user

issue_router = APIRouter(tags=["issue"])

logger = logging.getLogger(__name__)


@issue_router.post(
    "/project/{id}/issue/", response_model=IssueSchema, status_code=status.HTTP_201_CREATED
)
@permissions(['project_user'])
async def create_issue(
        id: int,
        payload: CreateIssue,
        user: dict = Depends(valid_user)
):
    logger.debug(f"Trying to create issue by user {user.get('id')}")
    print(payload.dict(exclude_unset=True))
    issue_instance = await Issue.create_issue(
        payload.dict(exclude_unset=True), project_id=id
    )
    return issue_instance


@issue_router.get("/project/{id}/issues", response_model=ProjectIssuesSchema)
@permissions(['project_user'])
async def get_project_issues(
        id: int,
        user: dict = Depends(valid_user)
):
    logger.debug(f"Trying to fetch issues for project {id} by user {user.get('id')}")
    issues = await Issue.filter(project_id=id)
    response = {}
    response['project'] = await Project.get_project_by_id_for_response(project_id=id)
    response['project_issues'] = issues
    return response


@issue_router.get("/project/{id}/issue/{issue_id}/", response_model=IssueSchema)
@permissions(['project_user'])
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
@permissions(['project_user'])
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
@permissions(['project_user'])
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


@issue_router.post("/project/{id}/issue/{issue_id}/issue-users", response_model=IssueSchema)
@permissions(["project_user"])
async def create_project_users(
        id: int,
        issue_id: int,
        payload: CreateIssueUser,
        user: dict = Depends(valid_user)
):
    logger.debug(f"Trying to create project_users in project {id} by user {user.get('id')}")
    await User.get_multiple_user_by_ids(payload.users)
    await ProjectUser.get_multiple_user_by_ids(payload.users, id)
    issue_instance = await Issue.get_issue_by_id(issue_id=issue_id)
    issue_users_list = []
    await IssueUser.filter(issue=issue_instance).delete()
    for issue_user in payload.users:
        issue_users_list.append(IssueUser(issue=issue_instance, user_id=issue_user))
    if issue_users_list:
        await IssueUser.bulk_create(issue_users_list)
    return issue_instance
