"""
Reading Progress endpoints - Track user reading progress
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.reading_progress import (
    ReadingProgress,
    ReadingProgressCreate,
    ReadingProgressUpdate
)
from app.services import reading_progress_service

router = APIRouter()


@router.post("/", response_model=ReadingProgress, status_code=status.HTTP_201_CREATED)
def create_or_update_progress(
    progress_in: ReadingProgressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create or update reading progress for a book
    
    - **book_id**: ID of the book being read
    - **chapter_id**: ID of the current chapter
    - **progress_percentage**: Reading progress (0-100%)
    
    If progress already exists for this book, it will be updated.
    """
    progress = reading_progress_service.create_or_update_reading_progress(
        db, current_user.id, progress_in
    )
    return progress


@router.get("/", response_model=List[ReadingProgress])
def get_my_reading_progress(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all reading progress for the current user
    """
    skip = (page - 1) * page_size
    progress_list = reading_progress_service.get_user_reading_progress(
        db, current_user.id, skip=skip, limit=page_size
    )
    return progress_list


@router.get("/book/{book_id}", response_model=ReadingProgress)
def get_book_progress(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get reading progress for a specific book
    """
    progress = reading_progress_service.get_reading_progress_by_user_and_book(
        db, current_user.id, book_id
    )
    
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reading progress not found"
        )
    
    return progress


@router.put("/{progress_id}", response_model=ReadingProgress)
def update_progress(
    progress_id: int,
    progress_update: ReadingProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update reading progress by ID
    """
    progress = reading_progress_service.get_reading_progress_by_id(
        db, progress_id, current_user.id
    )
    
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reading progress not found"
        )
    
    updated_progress = reading_progress_service.update_reading_progress(
        db, progress, progress_update
    )
    return updated_progress


@router.delete("/{progress_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_progress(
    progress_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete reading progress by ID
    """
    progress = reading_progress_service.get_reading_progress_by_id(
        db, progress_id, current_user.id
    )
    
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reading progress not found"
        )
    
    reading_progress_service.delete_reading_progress(db, progress)
    return None


