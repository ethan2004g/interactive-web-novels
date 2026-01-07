"""
Bookmark Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


# Shared properties
class BookmarkBase(BaseModel):
    """Base bookmark schema with common fields"""
    book_id: int = Field(..., gt=0)


# Properties to receive via API on creation
class BookmarkCreate(BookmarkBase):
    """Schema for bookmark creation"""
    pass


# Properties shared by models stored in DB
class BookmarkInDBBase(BookmarkBase):
    """Base schema for bookmark data from database"""
    id: int
    user_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class Bookmark(BookmarkInDBBase):
    """Schema for bookmark response"""
    pass


# Schema for bookmark with book details
class BookmarkWithDetails(Bookmark):
    """Schema for bookmark with book details"""
    book_title: str
    book_cover_image_url: Optional[str]
    author_username: str
    
    model_config = ConfigDict(from_attributes=True)

