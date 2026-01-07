"""
Bookmarks endpoints - User bookmarks for books
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.bookmark import Bookmark, BookmarkCreate
from app.services import bookmark_service

router = APIRouter()


@router.post("/", response_model=Bookmark, status_code=status.HTTP_201_CREATED)
def create_bookmark(
    bookmark_in: BookmarkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a bookmark for a book
    
    - **book_id**: ID of the book to bookmark
    
    If the bookmark already exists, returns the existing bookmark.
    """
    bookmark = bookmark_service.create_bookmark(db, current_user.id, bookmark_in)
    return bookmark


@router.get("/", response_model=List[Bookmark])
def get_my_bookmarks(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all bookmarks for the current user
    """
    skip = (page - 1) * page_size
    bookmarks = bookmark_service.get_user_bookmarks(
        db, current_user.id, skip=skip, limit=page_size
    )
    return bookmarks


@router.get("/book/{book_id}", response_model=Bookmark)
def check_bookmark(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Check if user has bookmarked a specific book
    """
    bookmark = bookmark_service.get_bookmark_by_user_and_book(
        db, current_user.id, book_id
    )
    
    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found"
        )
    
    return bookmark


@router.delete("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bookmark(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a bookmark by book ID
    """
    success = bookmark_service.delete_bookmark_by_book(db, current_user.id, book_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found"
        )
    
    return None


