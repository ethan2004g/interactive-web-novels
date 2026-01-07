"""
Comments endpoints - User comments on chapters
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.comment import Comment, CommentCreate, CommentUpdate
from app.services import comment_service

router = APIRouter()


@router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED)
def create_comment(
    comment_in: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new comment on a chapter
    
    - **chapter_id**: ID of the chapter to comment on
    - **content**: Comment content (max 2000 characters)
    - **parent_comment_id**: Optional ID of parent comment for replies
    """
    comment = comment_service.create_comment(db, current_user.id, comment_in)
    return comment


@router.get("/chapter/{chapter_id}", response_model=List[Comment])
def get_chapter_comments(
    chapter_id: int,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    Get all top-level comments for a chapter (public endpoint)
    
    Does not include replies - use the /comments/{comment_id}/replies endpoint to get replies
    """
    skip = (page - 1) * page_size
    comments = comment_service.get_chapter_comments(
        db, chapter_id, skip=skip, limit=page_size
    )
    return comments


@router.get("/{comment_id}/replies", response_model=List[Comment])
def get_comment_replies(
    comment_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all replies to a specific comment
    """
    replies = comment_service.get_comment_replies(db, comment_id)
    return replies


@router.get("/my-comments", response_model=List[Comment])
def get_my_comments(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all comments by the current user
    """
    skip = (page - 1) * page_size
    comments = comment_service.get_user_comments(
        db, current_user.id, skip=skip, limit=page_size
    )
    return comments


@router.put("/{comment_id}", response_model=Comment)
def update_comment(
    comment_id: int,
    comment_update: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a comment (only by the comment author)
    """
    comment = comment_service.get_comment_by_id(db, comment_id)
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    # Check if user owns the comment
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this comment"
        )
    
    updated_comment = comment_service.update_comment(db, comment, comment_update)
    return updated_comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a comment (only by the comment author)
    
    Note: This will also delete all replies to this comment (cascade)
    """
    comment = comment_service.get_comment_by_id(db, comment_id)
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    # Check if user owns the comment
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this comment"
        )
    
    comment_service.delete_comment(db, comment)
    return None


@router.get("/chapter/{chapter_id}/count")
def get_chapter_comments_count(
    chapter_id: int,
    db: Session = Depends(get_db)
):
    """
    Get the total number of comments for a chapter
    """
    count = comment_service.get_chapter_comments_count(db, chapter_id)
    return {"chapter_id": chapter_id, "total_comments": count}


