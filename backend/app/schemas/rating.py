"""
Rating Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


# Shared properties
class RatingBase(BaseModel):
    """Base rating schema with common fields"""
    book_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)


# Properties to receive via API on creation
class RatingCreate(RatingBase):
    """Schema for rating creation"""
    pass


# Properties to receive via API on update
class RatingUpdate(BaseModel):
    """Schema for rating update"""
    rating: int = Field(..., ge=1, le=5)


# Properties shared by models stored in DB
class RatingInDBBase(RatingBase):
    """Base schema for rating data from database"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class Rating(RatingInDBBase):
    """Schema for rating response"""
    pass


# Schema for book rating statistics
class BookRatingStats(BaseModel):
    """Schema for book rating statistics"""
    book_id: int
    average_rating: float
    total_ratings: int
    rating_distribution: dict  # {1: count, 2: count, ...}

