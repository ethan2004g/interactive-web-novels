"""
Reading Progress model
"""
from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base


class ReadingProgress(Base):
    """Reading Progress model for tracking user reading progress"""
    __tablename__ = "reading_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False, index=True)
    progress_percentage = Column(Float, default=0.0, nullable=False)  # 0.0 to 100.0
    last_read_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", backref="reading_progress")
    book = relationship("Book", backref="reading_progress")
    chapter = relationship("Chapter", backref="reading_progress")
    
    def __repr__(self):
        return f"<ReadingProgress user={self.user_id} book={self.book_id} chapter={self.chapter_id} {self.progress_percentage}%>"


