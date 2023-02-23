import logging
from functools import wraps, update_wrapper
from typing import Union, List

from fastapi import HTTPException
from starlette import status

# from apps.issues.models import IssueUser
# from apps.projects.models import ProjectUser
from core.constants import UserType

logger = logging.getLogger(__name__)


def permissions(users: Union[List[str], None, str] = None,):
    def decorator_auth(func):
        @wraps(func)
        async def wrapper_auth(*args, **kwargs):
            valid_user = kwargs['user']
            id = kwargs.get('id')
            if UserType.PROJECT_USER.value in users:
                from apps.projects.models import ProjectUser
                project_user = ProjectUser.filter(user_id=valid_user.get('id'))
                if id:
                    project_user = project_user.filter(project_id=id)
                if not project_user.first() and not valid_user.get('is_superuser'):
                    raise HTTPException(
                                status_code=status.HTTP_403_FORBIDDEN,
                                detail="Invalid Credentials"
                            )
            if UserType.ISSUE_USER.value in users:
                from apps.issues.models import IssueUser
                issue_user = IssueUser.filter(user_id=valid_user.get('id'))
                if id:
                    issue_user = issue_user.filter(issue_id=id)
                if not issue_user.first() and not valid_user.get('is_superuser'):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Invalid Credentials"
                    )
            return await func(*args, **kwargs)

        return update_wrapper(wrapper_auth, func)

    return decorator_auth

