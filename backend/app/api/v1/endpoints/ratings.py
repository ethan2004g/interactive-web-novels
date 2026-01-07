"""
Ratings endpoints - User ratings for books
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.rating import Rating, RatingCreate, RatingUpdate, BookRatingStats
from app.services import rating_service

router = APIRouter()


@router.post("/", response_model=Rating, status_code=status.HTTP_201_CREATED)
def create_or_update_rating(
    rating_in: RatingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create or update a rating for a book
    
    - **book_id**: ID of the book to rate
    - **rating**: Rating value (1-5 stars)
    
    If a rating already exists for this book, it will be updated.
    """
    rating = rating_service.create_or_update_rating(db, current_user.id, rating_in)
    return rating


@router.get("/book/{book_id}", response_model=Rating)
def get_my_rating(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get the current user's rating for a specific book
    """
    rating = rating_service.get_rating_by_user_and_book(
        db, current_user.id, book_id
    )
    
    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found"
        )
    
    return rating


@router.get("/book/{book_id}/stats", response_model=BookRatingStats)
def get_book_rating_stats(
    book_id: int,
    db: Session = Depends(get_db)
):
    """
    Get rating statistics for a book (public endpoint)
    
    Returns:
    - Average rating
    - Total number of ratings
    - Rating distribution (1-5 stars)
    """
    stats = rating_service.get_book_rating_stats(db, book_id)
    return stats


@router.put("/book/{book_id}", response_model=Rating)
def update_rating(
    book_id: int,
    rating_update: RatingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing rating for a book
    """
    rating = rating_service.get_rating_by_user_and_book(
        db, current_user.id, book_id
    )
    
    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found"
        )
    
    updated_rating = rating_service.update_rating(db, rating, rating_update)
    return updated_rating


@router.delete("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rating(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a rating for a book
    """
    success = rating_service.delete_rating_by_book(db, current_user.id, book_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found"
        )
    
    return None


