"""
Bookmark service layer - Business logic for bookmark operations
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.bookmark import Bookmark
from app.schemas.bookmark import BookmarkCreate


def get_bookmark_by_user_and_book(
    db: Session, user_id: int, book_id: int
) -> Optional[Bookmark]:
    """Check if user has bookmarked a book"""
    return db.query(Bookmark).filter(
        and_(
            Bookmark.user_id == user_id,
            Bookmark.book_id == book_id
        )
    ).first()


def get_user_bookmarks(
    db: Session, user_id: int, skip: int = 0, limit: int = 20
) -> List[Bookmark]:
    """Get all bookmarks for a user"""
    return db.query(Bookmark).filter(
        Bookmark.user_id == user_id
    ).order_by(Bookmark.created_at.desc()).offset(skip).limit(limit).all()


def create_bookmark(db: Session, user_id: int, bookmark_in: BookmarkCreate) -> Bookmark:
    """Create a new bookmark"""
    # Check if bookmark already exists
    existing = get_bookmark_by_user_and_book(db, user_id, bookmark_in.book_id)
    if existing:
        return existing
    
    db_bookmark = Bookmark(
        user_id=user_id,
        book_id=bookmark_in.book_id
    )
    
    db.add(db_bookmark)
    db.commit()
    db.refresh(db_bookmark)
    return db_bookmark


def delete_bookmark(db: Session, bookmark: Bookmark) -> bool:
    """Delete a bookmark"""
    db.delete(bookmark)
    db.commit()
    return True


def delete_bookmark_by_book(db: Session, user_id: int, book_id: int) -> bool:
    """Delete a bookmark by user and book ID"""
    bookmark = get_bookmark_by_user_and_book(db, user_id, book_id)
    if bookmark:
        return delete_bookmark(db, bookmark)
    return False


