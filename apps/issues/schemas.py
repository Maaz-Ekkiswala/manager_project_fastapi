from typing import Optional, List

from pydantic import BaseModel

from apps.issues.constants import Type, Status, Priority


class IssueSchema(BaseModel):
    id: int
    title: str
    type: Type
    status: Status
    priority: Priority
    description: Optional[str]
    project_id: int
    issue_users: Optional[List[int]]


class CreateIssue(BaseModel):
    title: str
    type: Optional[Type]
    status: Optional[Status]
    priority: Optional[Priority]
    description: Optional[str]


class UpdatePutIssue(BaseModel):
    title: str
    type: Type
    status: Status
    priority: Priority
    description: str


class UpdateIssue(BaseModel):
    title: Optional[str]
    type: Optional[Type]
    status: Optional[Status]
    priority: Optional[Priority]
    description: Optional[str]
    is_active: Optional[bool]


class CreateIssueUser(BaseModel):
    users: List[int]