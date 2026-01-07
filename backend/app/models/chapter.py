"""
Chapter model
"""
from sqlalchemy import Column, Integer, String, Text, Enum as SQLEnum, ForeignKey, Boolean, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.base_class import Base


class ContentType(str, enum.Enum):
    """Chapter content type enumeration"""
    SIMPLE = "simple"
    INTERACTIVE = "interactive"


class Chapter(Base):
    """Chapter model for storing book chapters"""
    __tablename__ = "chapters"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, index=True)
    chapter_number = Column(Integer, nullable=False, index=True)
    title = Column(String(200), nullable=False)
    content_type = Column(SQLEnum(ContentType), default=ContentType.SIMPLE, nullable=False)
    content_data = Column(JSON, nullable=False)  # Stores either plain text or interactive JSON
    word_count = Column(Integer, default=0, nullable=False)
    is_published = Column(Boolean, default=False, nullable=False, index=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    book = relationship("Book", back_populates="chapters")
    # reading_progress = relationship("ReadingProgress", back_populates="chapter")
    # comments = relationship("Comment", back_populates="chapter")
    
    def __repr__(self):
        return f"<Chapter {self.chapter_number}: {self.title} (book_id={self.book_id})>"

