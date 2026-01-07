"""
Chapter Template Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime


# Shared properties
class ChapterTemplateBase(BaseModel):
    """Base chapter template schema with common fields"""
    name: str = Field(..., min_length=1, max_length=100, description="Template name")
    description: Optional[str] = Field(None, max_length=2000, description="Template description")
    preview_image_url: Optional[str] = Field(None, max_length=500, description="URL to preview image")
    template_data: Dict[str, Any] = Field(..., description="Template structure (JSON)")
    is_public: bool = Field(False, description="Whether template is publicly available")


# Properties to receive via API on creation
class ChapterTemplateCreate(ChapterTemplateBase):
    """Schema for chapter template creation"""
    
    @field_validator('template_data')
    @classmethod
    def validate_template_data(cls, v):
        """Validate template_data structure"""
        if not v:
            raise ValueError("template_data cannot be empty")
        
        # Basic validation - template should have some structure
        # Can be expanded based on specific requirements
        if not isinstance(v, dict):
            raise ValueError("template_data must be a dictionary")
        
        return v


# Properties to receive via API on update
class ChapterTemplateUpdate(BaseModel):
    """Schema for chapter template update"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=2000)
    preview_image_url: Optional[str] = Field(None, max_length=500)
    template_data: Optional[Dict[str, Any]] = None
    is_public: Optional[bool] = None


# Properties shared by models stored in DB
class ChapterTemplateInDBBase(ChapterTemplateBase):
    """Base schema for chapter template data from database"""
    id: int
    created_by: int
    usage_count: int = 0
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class ChapterTemplate(ChapterTemplateInDBBase):
    """Schema for chapter template response"""
    pass


# Schema with creator info
class ChapterTemplateWithCreator(ChapterTemplateInDBBase):
    """Schema for chapter template response with creator information"""
    creator_username: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


# Minimal template info (for lists)
class ChapterTemplateSummary(BaseModel):
    """Schema for chapter template summary (without full template_data)"""
    id: int
    name: str
    description: Optional[str] = None
    preview_image_url: Optional[str] = None
    created_by: int
    is_public: bool
    usage_count: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Schema for template list response
class ChapterTemplateListResponse(BaseModel):
    """Schema for chapter template list response"""
    templates: List[ChapterTemplateSummary]
    total: int

