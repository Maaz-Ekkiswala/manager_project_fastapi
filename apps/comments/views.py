import logging
from typing import List

from fastapi import APIRouter, Depends, Query
from starlette import status

from apps.comments.models import Comment
from apps.comments.schemas import CommentSchema, CreateComment, UpdateComment
from core.permissions import permissions
from core.valid_user import valid_user

comment_router = APIRouter(tags=["comment"])

logger = logging.getLogger(__name__)


@comment_router.post(
    "/issue/{id}/comment/", response_model=CommentSchema, status_code=status.HTTP_201_CREATED
)
@permissions(['project_user'])
async def create_comment(
        id: int,
        payload: CreateComment,
        user: dict = Depends(valid_user)
):
    logger.debug(f"Trying to create comment by user {user.get('id')}")
    comment_instance = await Comment.create_comment(
        **payload.dict(exclude_unset=True), issue_id=id
    )
    logger.debug(f"Comment created successfully {comment_instance.__dict__}")
    return comment_instance


@comment_router.get("/issue/{id}/comments", response_model=List[CommentSchema])
async def get_comments(
        id: int,
        only_my_comments: bool = Query(""),
        user: dict = Depends(valid_user)
):
    logger.debug(f"Trying to get list of comments by user {user.get('id')}")
    comments = await Comment.filter(issue_id=id)
    if only_my_comments:
        comments = await Comment.filter(issue_id=id, commented_by_id=user.get('id'))
    logger.debug(f"comments {len(comments)} retrieved successfully")
    return comments


@comment_router.put("/issue/{id}/comment/{comment_id}/", response_model=CommentSchema)
async def update_comment(
        id: int,
        comment_id: int,
        payload: UpdateComment,
        user: dict = Depends(valid_user)
):
    logger.debug(f"Trying to update comment by user {user.get('id')}")
    comment = await Comment.get_comment_by_id_with_issue(
        issue_id=id, comment_id=comment_id, logged_in_user=user.get('id')
    )
    updated_comment = await comment.update_from_dict(data=payload.dict(exclude_unset=True))
    return updated_comment


@comment_router.delete("/issue/{id}/comments/{comment_id}")
async def delete_comment(
        id: int,
        comment_id: int,
        user: dict = Depends(valid_user)
):
    logger.debug(f"Trying to delete comment by user {user.get('id')}")
    comment = await Comment.get_comment_by_id_with_issue(
        issue_id=id, comment_id=comment_id, logged_in_user=user.get('id')
    )
    comment.delete()
    return "comment deleted successfully"
