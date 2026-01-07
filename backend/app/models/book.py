"""
Book model
"""
from sqlalchemy import Column, Integer, String, Text, Enum as SQLEnum, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base


class BookStatus(str, enum.Enum):
    """Book status enumeration"""
    DRAFT = "draft"
    ONGOING = "ongoing"
    COMPLETED = "completed"


class Book(Base):
    """Book model for storing book information"""
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    cover_image_url = Column(String(500), nullable=True)
    thumbnail_url = Column(String(500), nullable=True)
    genre = Column(String(100), nullable=True, index=True)
    tags = Column(ARRAY(String), nullable=True)  # Array of tags
    status = Column(SQLEnum(BookStatus), default=BookStatus.DRAFT, nullable=False, index=True)
    total_views = Column(Integer, default=0, nullable=False)
    total_likes = Column(Integer, default=0, nullable=False)
    
    # Relationships
    author = relationship("User", back_populates="books")
    chapters = relationship("Chapter", back_populates="book", cascade="all, delete-orphan")
    # reading_progress = relationship("ReadingProgress", back_populates="book")
    # bookmarks = relationship("Bookmark", back_populates="book")
    # ratings = relationship("Rating", back_populates="book")
    
    def __repr__(self):
        return f"<Book {self.title} by author_id={self.author_id}>"

