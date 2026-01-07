"""
Chapter Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.chapter import ContentType


# Shared properties
class ChapterBase(BaseModel):
    """Base chapter schema with common fields"""
    title: str = Field(..., min_length=1, max_length=200)
    chapter_number: int = Field(..., ge=1, description="Chapter number (1-indexed)")
    content_type: ContentType = ContentType.SIMPLE
    content_data: Dict[str, Any] = Field(..., description="Chapter content (text or interactive JSON)")
    is_published: bool = False


# Properties to receive via API on creation
class ChapterCreate(ChapterBase):
    """Schema for chapter creation"""
    
    @field_validator('content_data')
    @classmethod
    def validate_content_data(cls, v, info):
        """Validate content_data structure"""
        if not v:
            raise ValueError("content_data cannot be empty")
        
        content_type = info.data.get('content_type', ContentType.SIMPLE)
        
        if content_type == ContentType.SIMPLE:
            # For simple chapters, expect {"text": "..."}
            if 'text' not in v:
                raise ValueError("Simple chapters must have 'text' field in content_data")
            if not isinstance(v['text'], str):
                raise ValueError("'text' field must be a string")
        elif content_type == ContentType.INTERACTIVE:
            # For interactive chapters, expect more complex structure
            # Basic validation - can be expanded based on your needs
            if 'nodes' not in v:
                raise ValueError("Interactive chapters must have 'nodes' field in content_data")
            if not isinstance(v['nodes'], list):
                raise ValueError("'nodes' field must be a list")
        
        return v


# Properties to receive via API on update
class ChapterUpdate(BaseModel):
    """Schema for chapter update"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    chapter_number: Optional[int] = Field(None, ge=1)
    content_type: Optional[ContentType] = None
    content_data: Optional[Dict[str, Any]] = None
    is_published: Optional[bool] = None


# Properties for chapter reordering
class ChapterReorder(BaseModel):
    """Schema for reordering chapters"""
    chapter_id: int
    new_chapter_number: int = Field(..., ge=1)


# Properties shared by models stored in DB
class ChapterInDBBase(ChapterBase):
    """Base schema for chapter data from database"""
    id: int
    book_id: int
    word_count: int = 0
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class Chapter(ChapterInDBBase):
    """Schema for chapter response"""
    pass


# Minimal chapter info (for lists)
class ChapterSummary(BaseModel):
    """Schema for chapter summary (without full content)"""
    id: int
    book_id: int
    chapter_number: int
    title: str
    content_type: ContentType
    word_count: int
    is_published: bool
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Schema for chapter list response
class ChapterListResponse(BaseModel):
    """Schema for chapter list response"""
    chapters: List[ChapterSummary]
    total: int

