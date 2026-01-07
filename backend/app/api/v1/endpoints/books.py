"""
Books endpoints - CRUD operations for books
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user, get_current_author
from app.models.user import User
from app.models.book import BookStatus
from app.schemas.book import Book, BookCreate, BookUpdate, BookListResponse
from app.services import book_service
import math

router = APIRouter()


@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(
    book_in: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_author)
):
    """
    Create a new book (Authors only)
    
    - **title**: Book title (required)
    - **description**: Book description
    - **cover_image_url**: URL to cover image
    - **genre**: Book genre
    - **tags**: Array of tags
    - **status**: Book status (draft/ongoing/completed)
    """
    book = book_service.create_book(db, book_in, current_user.id)
    return book


@router.get("/", response_model=BookListResponse)
def get_books(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    author_id: Optional[int] = Query(None, description="Filter by author ID"),
    status: Optional[BookStatus] = Query(None, description="Filter by status"),
    genre: Optional[str] = Query(None, description="Filter by genre"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    tags: Optional[str] = Query(None, description="Comma-separated tags to filter by"),
    db: Session = Depends(get_db)
):
    """
    Get all books with pagination and filtering
    
    Filters:
    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 20, max: 100)
    - **author_id**: Filter by author ID
    - **status**: Filter by status (draft/ongoing/completed)
    - **genre**: Filter by genre
    - **search**: Search in title and description
    - **tags**: Comma-separated tags (e.g., "fantasy,adventure")
    """
    skip = (page - 1) * page_size
    
    # Parse tags
    tags_list = None
    if tags:
        tags_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
    
    books, total = book_service.get_books(
        db,
        skip=skip,
        limit=page_size,
        author_id=author_id,
        status=status,
        genre=genre,
        search=search,
        tags=tags_list
    )
    
    total_pages = math.ceil(total / page_size) if total > 0 else 0
    
    return {
        "books": books,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


@router.get("/my-books", response_model=List[Book])
def get_my_books(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_author)
):
    """
    Get all books by the current authenticated author
    
    Requires author role
    """
    books = book_service.get_user_books(db, current_user.id)
    return books


@router.get("/{book_id}", response_model=Book)
def get_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a single book by ID
    
    Does not require authentication
    """
    book = book_service.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    # Increment view count
    book_service.increment_views(db, book)
    
    return book


@router.put("/{book_id}", response_model=Book)
def update_book(
    book_id: int,
    book_update: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_author)
):
    """
    Update a book (Author only - must be book owner)
    
    - **title**: Updated title
    - **description**: Updated description
    - **cover_image_url**: Updated cover image URL
    - **genre**: Updated genre
    - **tags**: Updated tags array
    - **status**: Updated status
    """
    book = book_service.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    # Check if user is the author
    if not book_service.is_book_author(book, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this book"
        )
    
    updated_book = book_service.update_book(db, book, book_update)
    return updated_book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_author)
):
    """
    Delete a book (Author only - must be book owner)
    
    This will also delete all chapters associated with the book
    """
    book = book_service.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    # Check if user is the author
    if not book_service.is_book_author(book, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this book"
        )
    
    book_service.delete_book(db, book)
    return None


@router.post("/{book_id}/like", response_model=Book)
def like_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Like a book
    
    Requires authentication
    Note: This is a simple like counter. For production, implement proper like tracking per user.
    """
    book = book_service.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    updated_book = book_service.increment_likes(db, book)
    return updated_book

