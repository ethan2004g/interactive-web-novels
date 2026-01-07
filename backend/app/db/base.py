"""
Database base configuration
Import all SQLAlchemy models here to make them available to Alembic
"""
from app.db.base_class import Base

# Import all models here for Alembic to detect them
from app.models.user import User
from app.models.book import Book
from app.models.chapter import Chapter
from app.models.reading_progress import ReadingProgress
from app.models.bookmark import Bookmark
from app.models.rating import Rating
from app.models.comment import Comment

