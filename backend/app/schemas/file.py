"""
Pydantic schemas for file uploads
"""
from pydantic import BaseModel
from typing import Optional


class ImageUploadResponse(BaseModel):
    """Response for image upload"""
    image_url: str
    thumbnail_url: Optional[str] = None
    filename: str
    message: str = "Image uploaded successfully"


class FileDeleteResponse(BaseModel):
    """Response for file deletion"""
    success: bool
    message: str

