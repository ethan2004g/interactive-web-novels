"""
Book service layer - Business logic for book operations
"""
from typing import Optional, List, Tuple, Dict
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from app.models.book import Book, BookStatus
from app.models.user import User
from app.models.chapter import Chapter
from app.models.comment import Comment
from app.models.bookmark import Bookmark
from app.models.rating import Rating
from app.schemas.book import BookCreate, BookUpdate


def get_book_by_id(db: Session, book_id: int) -> Optional[Book]:
    """Get book by ID"""
    return db.query(Book).filter(Book.id == book_id).first()


def get_books(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    author_id: Optional[int] = None,
    status: Optional[BookStatus] = None,
    genre: Optional[str] = None,
    search: Optional[str] = None,
    tags: Optional[List[str]] = None
) -> Tuple[List[Book], int]:
    """
    Get books with filtering and pagination
    Returns tuple of (books, total_count)
    """
    query = db.query(Book)
    
    # Apply filters
    if author_id is not None:
        query = query.filter(Book.author_id == author_id)
    
    if status is not None:
        query = query.filter(Book.status == status)
    
    if genre is not None:
        query = query.filter(Book.genre == genre)
    
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                Book.title.ilike(search_pattern),
                Book.description.ilike(search_pattern)
            )
        )
    
    if tags and len(tags) > 0:
        # Filter books that have any of the specified tags
        # Using overlap operator for PostgreSQL arrays
        query = query.filter(Book.tags.bool_op("&&")(tags))
    
    # Get total count before pagination
    total = query.count()
    
    # Apply pagination and ordering
    books = query.order_by(Book.created_at.desc()).offset(skip).limit(limit).all()
    
    return books, total


def create_book(db: Session, book_in: BookCreate, author_id: int) -> Book:
    """Create a new book"""
    db_book = Book(
        **book_in.model_dump(),
        author_id=author_id
    )
    
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book: Book, book_update: BookUpdate) -> Book:
    """Update a book"""
    update_data = book_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(book, field, value)
    
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book: Book) -> bool:
    """Delete a book"""
    db.delete(book)
    db.commit()
    return True


def increment_views(db: Session, book: Book) -> Book:
    """Increment book view count"""
    book.total_views += 1
    db.commit()
    db.refresh(book)
    return book


def increment_likes(db: Session, book: Book) -> Book:
    """Increment book likes count"""
    book.total_likes += 1
    db.commit()
    db.refresh(book)
    return book


def get_user_books(db: Session, user_id: int) -> List[Book]:
    """Get all books by a specific user"""
    return db.query(Book).filter(Book.author_id == user_id).order_by(Book.created_at.desc()).all()


def is_book_author(book: Book, user: User) -> bool:
    """Check if user is the author of the book"""
    return book.author_id == user.id


def get_book_statistics(db: Session, book_id: int) -> Dict:
    """Get comprehensive statistics for a book"""
    # Get the book
    book = get_book_by_id(db, book_id)
    if not book:
        return None
    
    # Get chapter count
    chapter_count = db.query(func.count(Chapter.id)).filter(Chapter.book_id == book_id).scalar()
    
    # Get total comments count across all chapters
    comment_count = db.query(func.count(Comment.id)).join(
        Chapter, Comment.chapter_id == Chapter.id
    ).filter(Chapter.book_id == book_id).scalar()
    
    # Get bookmark count
    bookmark_count = db.query(func.count(Bookmark.id)).filter(Bookmark.book_id == book_id).scalar()
    
    # Get rating statistics
    rating_stats = db.query(
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
        "total_views": book.total_views,
        "total_likes": book.total_likes,
        "total_chapters": chapter_count or 0,
        "total_comments": comment_count or 0,
        "total_bookmarks": bookmark_count or 0,
        "average_rating": float(rating_stats.average) if rating_stats.average else 0.0,
        "total_ratings": rating_stats.total if rating_stats.total else 0,
        "rating_distribution": rating_dist
    }

