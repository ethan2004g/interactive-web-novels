"""
File storage utilities for handling uploads
"""
import os
import uuid
import shutil
from pathlib import Path
from typing import Optional
from datetime import datetime
from PIL import Image
import aiofiles

from app.core.config import settings


class FileStorage:
    """Handle file storage operations"""
    
    # Define storage directories
    UPLOAD_DIR = Path("uploads")
    IMAGES_DIR = UPLOAD_DIR / "images"
    COVERS_DIR = IMAGES_DIR / "covers"
    CHAPTERS_DIR = IMAGES_DIR / "chapters"
    THUMBNAILS_DIR = IMAGES_DIR / "thumbnails"
    
    # File validation constants
    ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    THUMBNAIL_SIZE = (300, 400)  # width x height for book covers
    
    @classmethod
    def init_storage(cls):
        """Initialize storage directories"""
        for directory in [cls.COVERS_DIR, cls.CHAPTERS_DIR, cls.THUMBNAILS_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def generate_filename(cls, original_filename: str) -> str:
        """Generate unique filename preserving extension"""
        ext = Path(original_filename).suffix.lower()
        unique_id = uuid.uuid4().hex
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        return f"{timestamp}_{unique_id}{ext}"
    
    @classmethod
    def validate_image(cls, filename: str, file_size: int) -> tuple[bool, Optional[str]]:
        """
        Validate image file
        Returns: (is_valid, error_message)
        """
        # Check file size
        if file_size > cls.MAX_FILE_SIZE:
            return False, f"File size exceeds maximum allowed size of {cls.MAX_FILE_SIZE / 1024 / 1024}MB"
        
        # Check file extension
        ext = Path(filename).suffix.lower()
        if ext not in cls.ALLOWED_IMAGE_EXTENSIONS:
            return False, f"File type not allowed. Allowed types: {', '.join(cls.ALLOWED_IMAGE_EXTENSIONS)}"
        
        return True, None
    
    @classmethod
    async def save_upload_file(cls, file, destination: Path) -> str:
        """
        Save uploaded file to destination
        Returns: saved file path
        """
        try:
            async with aiofiles.open(destination, 'wb') as out_file:
                content = await file.read()
                await out_file.write(content)
            return str(destination)
        finally:
            await file.close()
    
    @classmethod
    def create_thumbnail(cls, image_path: Path, thumbnail_path: Path, size: tuple = None) -> str:
        """
        Create thumbnail from image
        Returns: thumbnail path
        """
        if size is None:
            size = cls.THUMBNAIL_SIZE
        
        try:
            with Image.open(image_path) as img:
                # Convert RGBA to RGB if necessary
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                
                # Create thumbnail maintaining aspect ratio
                img.thumbnail(size, Image.Resampling.LANCZOS)
                
                # Save thumbnail
                img.save(thumbnail_path, quality=85, optimize=True)
            
            return str(thumbnail_path)
        except Exception as e:
            raise Exception(f"Failed to create thumbnail: {str(e)}")
    
    @classmethod
    async def save_cover_image(cls, file, filename: str) -> dict:
        """
        Save book cover image and create thumbnail
        Returns: dict with image_url and thumbnail_url
        """
        # Save original image
        image_path = cls.COVERS_DIR / filename
        await cls.save_upload_file(file, image_path)
        
        # Create thumbnail
        thumbnail_filename = f"thumb_{filename}"
        thumbnail_path = cls.THUMBNAILS_DIR / thumbnail_filename
        cls.create_thumbnail(image_path, thumbnail_path)
        
        return {
            "image_url": f"/uploads/images/covers/{filename}",
            "thumbnail_url": f"/uploads/images/thumbnails/{thumbnail_filename}"
        }
    
    @classmethod
    async def save_chapter_image(cls, file, filename: str) -> dict:
        """
        Save chapter image
        Returns: dict with image_url
        """
        # Save image
        image_path = cls.CHAPTERS_DIR / filename
        await cls.save_upload_file(file, image_path)
        
        return {
            "image_url": f"/uploads/images/chapters/{filename}"
        }
    
    @classmethod
    def delete_file(cls, file_path: str) -> bool:
        """Delete a file from storage"""
        try:
            # Convert URL path to filesystem path
            if file_path.startswith("/uploads/"):
                file_path = file_path[1:]  # Remove leading slash
            
            full_path = Path(file_path)
            if full_path.exists():
                full_path.unlink()
                return True
            return False
        except Exception:
            return False
    
    @classmethod
    def delete_cover_with_thumbnail(cls, cover_url: str, thumbnail_url: str = None) -> bool:
        """Delete cover image and its thumbnail"""
        success = cls.delete_file(cover_url)
        if thumbnail_url:
            cls.delete_file(thumbnail_url)
        return success


# Initialize storage on module import
FileStorage.init_storage()

