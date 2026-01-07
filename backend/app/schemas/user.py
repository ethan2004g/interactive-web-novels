"""
User Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.user import UserRole


# Shared properties
class UserBase(BaseModel):
    """Base user schema with common fields"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    role: UserRole = UserRole.READER


# Properties to receive via API on creation
class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=8, max_length=100)


# Properties to receive via API on update
class UserUpdate(BaseModel):
    """Schema for user profile update"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    bio: Optional[str] = Field(None, max_length=1000)
    profile_picture_url: Optional[str] = Field(None, max_length=500)


# Properties to receive via API on password change
class UserPasswordUpdate(BaseModel):
    """Schema for password change"""
    old_password: str = Field(..., min_length=8, max_length=100)
    new_password: str = Field(..., min_length=8, max_length=100)


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    """Base schema for user data from database"""
    id: int
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class User(UserInDBBase):
    """Schema for user response (public data)"""
    pass


# Properties stored in DB
class UserInDB(UserInDBBase):
    """Schema for user in database (includes password hash)"""
    password_hash: str


# Authentication schemas
class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Schema for JWT token payload"""
    sub: Optional[str] = None  # subject: user id (JWT spec requires string)
    type: Optional[str] = None  # token type: access or refresh
    exp: Optional[int] = None  # expiration time
    
    model_config = ConfigDict(extra='allow')  # Allow extra fields from JWT

