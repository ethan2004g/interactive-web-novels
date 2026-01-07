"""
Rating service layer - Business logic for rating operations
"""
from typing import Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app.models.rating import Rating
from app.schemas.rating import RatingCreate, RatingUpdate


def get_rating_by_user_and_book(
    db: Session, user_id: int, book_id: int
) -> Optional[Rating]:
    """Get rating by user and book"""
    return db.query(Rating).filter(
        and_(
            Rating.user_id == user_id,
            Rating.book_id == book_id
        )
    ).first()


def get_book_rating_stats(db: Session, book_id: int) -> Dict:
    """Get rating statistics for a book"""
    # Get average rating and total count
    stats = db.query(
        func.avg(Rating.rating).label('average'),
        func.count(Rating.id).label('total')
    ).filter(Rating.book_id == book_id).first()
    
    # Get rating distribution
    distribution = db.query(
        Rating.rating,
        func.count(Rating.id)
    ).filter(Rating.book_id == book_id).group_by(Rating.rating).all()
    
    rating_dist = {i: 0 for i in range(1, 6)}  # Initialize 1-5 stars with 0
    for rating_value, count in distribution:
        rating_dist[rating_value] = count
    
    return {
        "book_id": book_id,
        "average_rating": float(stats.average) if stats.average else 0.0,
        "total_ratings": stats.total if stats.total else 0,
        "rating_distribution": rating_dist
    }


def create_or_update_rating(
    db: Session, user_id: int, rating_in: RatingCreate
) -> Rating:
    """Create or update a rating"""
    # Check if rating already exists
    existing_rating = get_rating_by_user_and_book(db, user_id, rating_in.book_id)
    
    if existing_rating:
        # Update existing rating
        existing_rating.rating = rating_in.rating
        db.commit()
        db.refresh(existing_rating)
        return existing_rating
    else:
        # Create new rating
        db_rating = Rating(
            user_id=user_id,
            **rating_in.model_dump()
        )
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
        return db_rating


def update_rating(db: Session, rating: Rating, rating_update: RatingUpdate) -> Rating:
    """Update a rating"""
    rating.rating = rating_update.rating
    db.commit()
    db.refresh(rating)
    return rating


def delete_rating(db: Session, rating: Rating) -> bool:
    """Delete a rating"""
    db.delete(rating)
    db.commit()
    return True


def delete_rating_by_book(db: Session, user_id: int, book_id: int) -> bool:
    """Delete a rating by user and book ID"""
    rating = get_rating_by_user_and_book(db, user_id, book_id)
    if rating:
        return delete_rating(db, rating)
    return False


