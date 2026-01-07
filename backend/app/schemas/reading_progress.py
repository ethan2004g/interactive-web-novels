"""
Reading Progress Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


# Shared properties
class ReadingProgressBase(BaseModel):
    """Base reading progress schema with common fields"""
    book_id: int = Field(..., gt=0)
    chapter_id: int = Field(..., gt=0)
    progress_percentage: float = Field(..., ge=0.0, le=100.0)


# Properties to receive via API on creation
class ReadingProgressCreate(ReadingProgressBase):
    """Schema for reading progress creation"""
    pass


# Properties to receive via API on update
class ReadingProgressUpdate(BaseModel):
    """Schema for reading progress update"""
    chapter_id: Optional[int] = Field(None, gt=0)
    progress_percentage: Optional[float] = Field(None, ge=0.0, le=100.0)


# Properties shared by models stored in DB
class ReadingProgressInDBBase(ReadingProgressBase):
    """Base schema for reading progress data from database"""
    id: int
    user_id: int
    last_read_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class ReadingProgress(ReadingProgressInDBBase):
    """Schema for reading progress response"""
    pass


# Schema for reading progress with additional details
class ReadingProgressWithDetails(ReadingProgress):
    """Schema for reading progress with book and chapter details"""
    book_title: str
    chapter_title: str
    
    model_config = ConfigDict(from_attributes=True)


