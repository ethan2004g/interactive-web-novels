"""
Reading Progress service layer - Business logic for reading progress operations
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.reading_progress import ReadingProgress
from app.schemas.reading_progress import ReadingProgressCreate, ReadingProgressUpdate


def get_reading_progress_by_user_and_book(
    db: Session, user_id: int, book_id: int
) -> Optional[ReadingProgress]:
    """Get reading progress for a user on a specific book"""
    return db.query(ReadingProgress).filter(
        and_(
            ReadingProgress.user_id == user_id,
            ReadingProgress.book_id == book_id
        )
    ).first()


def get_reading_progress_by_id(
    db: Session, progress_id: int, user_id: int
) -> Optional[ReadingProgress]:
    """Get reading progress by ID (user-specific)"""
    return db.query(ReadingProgress).filter(
        and_(
            ReadingProgress.id == progress_id,
            ReadingProgress.user_id == user_id
        )
    ).first()


def get_user_reading_progress(
    db: Session, user_id: int, skip: int = 0, limit: int = 20
) -> List[ReadingProgress]:
    """Get all reading progress for a user"""
    return db.query(ReadingProgress).filter(
        ReadingProgress.user_id == user_id
    ).order_by(ReadingProgress.last_read_at.desc()).offset(skip).limit(limit).all()


def create_or_update_reading_progress(
    db: Session, user_id: int, progress_in: ReadingProgressCreate
) -> ReadingProgress:
    """Create or update reading progress for a user"""
    # Check if progress already exists for this user and book
    existing_progress = get_reading_progress_by_user_and_book(
        db, user_id, progress_in.book_id
    )
    
    if existing_progress:
        # Update existing progress
        existing_progress.chapter_id = progress_in.chapter_id
        existing_progress.progress_percentage = progress_in.progress_percentage
        db.commit()
        db.refresh(existing_progress)
        return existing_progress
    else:
        # Create new progress
        db_progress = ReadingProgress(
            user_id=user_id,
            **progress_in.model_dump()
        )
        db.add(db_progress)
        db.commit()
        db.refresh(db_progress)
        return db_progress


def update_reading_progress(
    db: Session, progress: ReadingProgress, progress_update: ReadingProgressUpdate
) -> ReadingProgress:
    """Update reading progress"""
    update_data = progress_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(progress, field, value)
    
    db.commit()
    db.refresh(progress)
    return progress


def delete_reading_progress(db: Session, progress: ReadingProgress) -> bool:
    """Delete reading progress"""
    db.delete(progress)
    db.commit()
    return True


