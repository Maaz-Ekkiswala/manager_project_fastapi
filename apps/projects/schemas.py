from typing import Optional, List

from pydantic import BaseModel

from apps.issues.schemas import IssueSchema
from apps.master.schemas import CategorySchema


class ProjectSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]
    url: str
    is_active: bool
    category_data: Optional[CategorySchema]


class UpdateProjectSchema(BaseModel):
    name: Optional[str]
    description: Optional[str]
    url: Optional[str]
    category_id: Optional[int]
    is_active: Optional[bool]


class UpdatePutProjectSchema(BaseModel):
    name: str
    description: str
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