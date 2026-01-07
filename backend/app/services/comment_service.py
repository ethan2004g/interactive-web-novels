"""
Comment service layer - Business logic for comment operations
"""
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate


def get_comment_by_id(db: Session, comment_id: int) -> Optional[Comment]:
    """Get comment by ID"""
    return db.query(Comment).filter(Comment.id == comment_id).first()


def get_chapter_comments(
    db: Session, chapter_id: int, skip: int = 0, limit: int = 50
) -> List[Comment]:
    """Get all top-level comments for a chapter (not replies)"""
    return db.query(Comment).filter(
        Comment.chapter_id == chapter_id,
        Comment.parent_comment_id.is_(None)
    ).order_by(Comment.created_at.desc()).offset(skip).limit(limit).all()


def get_comment_replies(db: Session, parent_comment_id: int) -> List[Comment]:
    """Get all replies to a comment"""
    return db.query(Comment).filter(
        Comment.parent_comment_id == parent_comment_id
    ).order_by(Comment.created_at.asc()).all()


def get_user_comments(
    db: Session, user_id: int, skip: int = 0, limit: int = 20
) -> List[Comment]:
    """Get all comments by a user"""
    return db.query(Comment).filter(
        Comment.user_id == user_id
    ).order_by(Comment.created_at.desc()).offset(skip).limit(limit).all()


def create_comment(db: Session, user_id: int, comment_in: CommentCreate) -> Comment:
    """Create a new comment"""
    db_comment = Comment(
        user_id=user_id,
        **comment_in.model_dump()
    )
    
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def update_comment(db: Session, comment: Comment, comment_update: CommentUpdate) -> Comment:
    """Update a comment"""
    comment.content = comment_update.content
    db.commit()
    db.refresh(comment)
    return comment


def delete_comment(db: Session, comment: Comment) -> bool:
    """Delete a comment (and all its replies via cascade)"""
    db.delete(comment)
    db.commit()
    return True


def get_chapter_comments_count(db: Session, chapter_id: int) -> int:
    """Get total comment count for a chapter (including replies)"""
    return db.query(Comment).filter(Comment.chapter_id == chapter_id).count()


