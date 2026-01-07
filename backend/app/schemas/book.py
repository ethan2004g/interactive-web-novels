"""
Book Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.models.book import BookStatus


# Shared properties
class BookBase(BaseModel):
    """Base book schema with common fields"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=5000)
    cover_image_url: Optional[str] = Field(None, max_length=500)
    thumbnail_url: Optional[str] = Field(None, max_length=500)
    genre: Optional[str] = Field(None, max_length=100)
    tags: Optional[List[str]] = Field(default_factory=list)
    status: BookStatus = BookStatus.DRAFT


# Properties to receive via API on creation
class BookCreate(BookBase):
    """Schema for book creation"""
    pass


# Properties to receive via API on update
class BookUpdate(BaseModel):
    """Schema for book update"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=5000)
    cover_image_url: Optional[str] = Field(None, max_length=500)
    thumbnail_url: Optional[str] = Field(None, max_length=500)
    genre: Optional[str] = Field(None, max_length=100)
    tags: Optional[List[str]] = None
    status: Optional[BookStatus] = None


# Properties shared by models stored in DB
class BookInDBBase(BookBase):
    """Base schema for book data from database"""
    id: int
    author_id: int
    total_views: int = 0
    total_likes: int = 0
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class Book(BookInDBBase):
    """Schema for book response"""
    pass


# Properties with author details
class BookWithAuthor(Book):
    """Schema for book response with author information"""
    author_username: str
    author_email: str
    
    model_config = ConfigDict(from_attributes=True)


# Schema for book list response with pagination
class BookListResponse(BaseModel):
    """Schema for paginated book list response"""
    books: List[Book]
    total: int
    page: int
    page_size: int
    total_pages: int


# Schema for comprehensive book statistics
class BookStatistics(BaseModel):
    """Schema for comprehensive book statistics"""
    book_id: int
    total_views: int
    total_likes: int
    total_chapters: int
    total_comments: int
    total_bookmarks: int
    average_rating: float
    total_ratings: int
    rating_distribution: dict