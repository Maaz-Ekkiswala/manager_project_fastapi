from typing import Optional

from pydantic import BaseModel

from apps.master.schemas import CategorySchema


class ProjectSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]
    url: str
    category_data: Optional[CategorySchema]


class CreateProject(BaseModel):
    name: str
    description: Optional[str]
    url: str
    category_id: int
