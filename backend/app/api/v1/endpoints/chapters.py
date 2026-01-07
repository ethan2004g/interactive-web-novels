"""
Chapters endpoints - CRUD operations for book chapters
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user, get_current_author
from app.models.user import User
from app.schemas.chapter import (
    Chapter, ChapterCreate, ChapterUpdate, ChapterSummary,
    ChapterListResponse, ChapterReorder
)
from app.services import chapter_service, book_service

router = APIRouter()


@router.post("/books/{book_id}/chapters", response_model=Chapter, status_code=status.HTTP_201_CREATED)
def create_chapter(
    book_id: int,
    chapter_in: ChapterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_author)
):
    """
    Create a new chapter for a book (Authors only - must be book owner)
    
    - **book_id**: ID of the book to add chapter to
    - **title**: Chapter title (required)
    - **chapter_number**: Chapter number (1-indexed)
    - **content_type**: simple or interactive
    - **content_data**: Chapter content (JSON format)
    - **is_published**: Whether chapter is published
    """
    # Check if book exists
    book = book_service.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    # Check if user is the book author
    if not book_service.is_book_author(book, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to add chapters to this book"
        )
    
    # Check if chapter number already exists
    existing_chapters = chapter_service.get_chapters_by_book(db, book_id)
    if any(ch.chapter_number == chapter_in.chapter_number for ch in existing_chapters):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Chapter number {chapter_in.chapter_number} already exists for this book"
        )
    
    chapter = chapter_service.create_chapter(db, chapter_in, book_id)
    return chapter


@router.get("/books/{book_id}/chapters", response_model=ChapterListResponse)
def get_book_chapters(
    book_id: int,
    published_only: bool = Query(False, description="Only return published chapters"),
    db: Session = Depends(get_db)
):
    """
    Get all chapters for a book
    
    - **book_id**: ID of the book
    - **published_only**: If true, only return published chapters (default: false)
    
    Note: This endpoint shows published chapters by default. Use published_only=false to see all chapters (requires authentication).
    """
    # Check if book exists
    book = book_service.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    # Get chapters (published only by default, or all if published_only=false)
    chapters = chapter_service.get_chapters_by_book(
        db, 
        book_id, 
        published_only=published_only if published_only else True
    )
    
    return {
        "chapters": chapters,
        "total": len(chapters)
    }


@router.get("/chapters/{chapter_id}", response_model=Chapter)
def get_chapter(
    chapter_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a single chapter by ID
    
    - **chapter_id**: ID of the chapter
    
    Note: Only published chapters can be accessed through this endpoint.
    """
    chapter = chapter_service.get_chapter_by_id(db, chapter_id)
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )
    
    # Only allow access to published chapters
    if not chapter.is_published:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This chapter is not published"
        )
    
    return chapter


@router.put("/chapters/{chapter_id}", response_model=Chapter)
def update_chapter(
    chapter_id: int,
    chapter_update: ChapterUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_author)
):
    """
    Update a chapter (Author only - must be book owner)
    
    - **chapter_id**: ID of the chapter to update
    - **title**: Updated title
    - **chapter_number**: Updated chapter number
    - **content_type**: Updated content type
    - **content_data**: Updated content
    - **is_published**: Updated published status
    """
    chapter = chapter_service.get_chapter_by_id(db, chapter_id)
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )
    
    # Check if user is the book author
    if not chapter_service.is_chapter_author(db, chapter, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this chapter"
        )
    
    # If updating chapter_number, check for conflicts
    if chapter_update.chapter_number is not None and chapter_update.chapter_number != chapter.chapter_number:
        existing_chapters = chapter_service.get_chapters_by_book(db, chapter.book_id)
        if any(ch.chapter_number == chapter_update.chapter_number and ch.id != chapter_id for ch in existing_chapters):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Chapter number {chapter_update.chapter_number} already exists for this book"
            )
    
    updated_chapter = chapter_service.update_chapter(db, chapter, chapter_update)
    return updated_chapter


@router.delete("/chapters/{chapter_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chapter(
    chapter_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_author)
):
    """
    Delete a chapter (Author only - must be book owner)
    
    - **chapter_id**: ID of the chapter to delete
    """
    chapter = chapter_service.get_chapter_by_id(db, chapter_id)
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )
    
    # Check if user is the book author
    if not chapter_service.is_chapter_author(db, chapter, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this chapter"
        )
    
    chapter_service.delete_chapter(db, chapter)
    return None


@router.post("/books/{book_id}/chapters/reorder", response_model=ChapterListResponse)
def reorder_chapters(
    book_id: int,
    reorder_data: ChapterReorder,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_author)
):
    """
    Reorder chapters within a book (Author only - must be book owner)
    
    Moves a chapter to a new position and adjusts other chapter numbers accordingly.
    
    - **book_id**: ID of the book
    - **chapter_id**: ID of the chapter to move
    - **new_chapter_number**: New position for the chapter (1-indexed)
    """
    # Check if book exists
    book = book_service.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    # Check if user is the book author
    if not book_service.is_book_author(book, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to reorder chapters for this book"
        )
    
    # Check if chapter belongs to this book
    chapter = chapter_service.get_chapter_by_id(db, reorder_data.chapter_id)
    if not chapter or chapter.book_id != book_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found in this book"
        )
    
    # Reorder chapters
    chapters = chapter_service.reorder_chapters(
        db, 
        book_id, 
        reorder_data.chapter_id, 
        reorder_data.new_chapter_number
    )
    
    if not chapters:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid chapter reordering operation"
        )
    
    return {
        "chapters": chapters,
        "total": len(chapters)
    }


@router.get("/books/{book_id}/chapters/next-number", response_model=dict)
def get_next_chapter_number(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_author)
):
    """
    Get the next available chapter number for a book (Author only - must be book owner)
    
    Useful when creating a new chapter to automatically assign the next sequential number.
    
    - **book_id**: ID of the book
    """
    # Check if book exists
    book = book_service.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    # Check if user is the book author
    if not book_service.is_book_author(book, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this book"
        )
    
    next_number = chapter_service.get_next_chapter_number(db, book_id)
    
    return {
        "book_id": book_id,
        "next_chapter_number": next_number
    }

