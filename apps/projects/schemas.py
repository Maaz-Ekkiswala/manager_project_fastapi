from typing import Optional, List

from pydantic import BaseModel, Field

from apps.issues.schemas import IssueSchema
from apps.master.schemas import CategorySchema


class ProjectSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]
    url: str
    is_active: bool
    _category: Optional[CategorySchema]
    project_users: Optional[List[int]]

    class Config:
        underscore_attrs_are_private = False


class ProjectDetailedSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]
    url: str
    is_active: bool
    category: CategorySchema
    project_users: List[int]
    issues: Optional[List[IssueSchema]]


class UpdateProjectSchema(BaseModel):
    name: Optional[str]
    description: Optional[str]
    url: Optional[str]
    category_id: Optional[int]
    is_active: Optional[bool]


class UpdatePutProjectSchema(BaseModel):
    name: str
    description: Optional[str]
    url: str
    category_id: int
    is_active: bool


class CreateProject(BaseModel):
    name: str
    description: Optional[str]
    url: str
    category_id: int


class ProjectIssuesSchema(BaseModel):
    project: ProjectSchema
    project_issues: Optional[List[IssueSchema]]


class CreateProjectUser(BaseModel):
    users: List[int]