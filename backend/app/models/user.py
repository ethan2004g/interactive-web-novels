"""
User model
"""
from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from app.db.base_class import Base


class UserRole(str, enum.Enum):
    """User role enumeration"""
    READER = "reader"
    AUTHOR = "author"
    ADMIN = "admin"


class User(Base):
    """User model for authentication and profiles"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.READER, nullable=False)
    profile_picture_url = Column(String(500), nullable=True)
    bio = Column(String(1000), nullable=True)
    
    # Relationships will be added as we create other models
    # books = relationship("Book", back_populates="author")
    # reading_progress = relationship("ReadingProgress", back_populates="user")
    # comments = relationship("Comment", back_populates="user")
    # bookmarks = relationship("Bookmark", back_populates="user")
    # ratings = relationship("Rating", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.username} ({self.role})>"

