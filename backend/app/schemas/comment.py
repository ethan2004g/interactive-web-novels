"""
Comment Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


# Shared properties
class CommentBase(BaseModel):
    """Base comment schema with common fields"""
    chapter_id: int = Field(..., gt=0)
    content: str = Field(..., min_length=1, max_length=2000)
    parent_comment_id: Optional[int] = Field(None, gt=0)


# Properties to receive via API on creation
class CommentCreate(CommentBase):
    """Schema for comment creation"""
    pass


# Properties to receive via API on update
class CommentUpdate(BaseModel):
    """Schema for comment update"""
    content: str = Field(..., min_length=1, max_length=2000)


# Properties shared by models stored in DB
class CommentInDBBase(BaseModel):
    """Base schema for comment data from database"""
    id: int
    user_id: int
    chapter_id: int
    parent_comment_id: Optional[int]
    content: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class Comment(CommentInDBBase):
    """Schema for comment response"""
    pass


# Schema for comment with user details and nested replies
class CommentWithDetails(Comment):
    """Schema for comment with user details"""
    username: str
    user_profile_picture_url: Optional[str]
    replies: List["CommentWithDetails"] = []
    
    model_config = ConfigDict(from_attributes=True)


# Schema for chapter comments response
class ChapterCommentsResponse(BaseModel):
    """Schema for chapter comments response"""
    comments: List[CommentWithDetails]
    total: int


