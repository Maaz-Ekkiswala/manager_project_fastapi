from typing import Optional

from pydantic import BaseModel


class CreateComment(BaseModel):
    issue_id: int
    commented_by_id: int
    description: str


class CommentSchema(BaseModel):
    id: int
    issue_id: int
    commented_by_id: int
    is_active: bool
    description: str


class UpdateComment(BaseModel):
    description: str
    is_active: Optional[bool]
