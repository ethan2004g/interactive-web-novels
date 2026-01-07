"""
File upload endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import Optional

from app.core.storage import FileStorage
from app.schemas.file import ImageUploadResponse, FileDeleteResponse
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.book import Book

router = APIRouter()


@router.post("/upload/cover", response_model=ImageUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_cover_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a book cover image
    - Validates file type and size
    - Creates thumbnail automatically
    - Returns URLs for both original and thumbnail
    """
    # Validate file
    file_size = 0
    content = await file.read()
    file_size = len(content)
    await file.seek(0)  # Reset file pointer
    
    is_valid, error_message = FileStorage.validate_image(file.filename, file_size)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message
        )
    
    # Generate unique filename
    filename = FileStorage.generate_filename(file.filename)
    
    try:
        # Save image and create thumbnail
        result = await FileStorage.save_cover_image(file, filename)
        
        return ImageUploadResponse(
            image_url=result["image_url"],
            thumbnail_url=result["thumbnail_url"],
            filename=filename,
            message="Cover image uploaded successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload image: {str(e)}"
        )


@router.post("/upload/chapter-image", response_model=ImageUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_chapter_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Upload an image for use in a chapter
    - Validates file type and size
    - Returns URL for the uploaded image
    """
    # Validate file
    file_size = 0
    content = await file.read()
    file_size = len(content)
    await file.seek(0)  # Reset file pointer
    
    is_valid, error_message = FileStorage.validate_image(file.filename, file_size)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message
        )
    
    # Generate unique filename
    filename = FileStorage.generate_filename(file.filename)
    
    try:
        # Save image
        result = await FileStorage.save_chapter_image(file, filename)
        
        return ImageUploadResponse(
            image_url=result["image_url"],
            thumbnail_url=None,
            filename=filename,
            message="Chapter image uploaded successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload image: {str(e)}"
        )


@router.delete("/delete", response_model=FileDeleteResponse)
async def delete_file(
    file_url: str,
    thumbnail_url: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Delete a file from storage
    - Optionally delete thumbnail as well
    - Only authenticated users can delete files
    """
    try:
        if thumbnail_url:
            success = FileStorage.delete_cover_with_thumbnail(file_url, thumbnail_url)
        else:
            success = FileStorage.delete_file(file_url)
        
        if success:
            return FileDeleteResponse(
                success=True,
                message="File deleted successfully"
            )
        else:
            return FileDeleteResponse(
                success=False,
                message="File not found or already deleted"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete file: {str(e)}"
        )


@router.get("/info")
async def get_upload_info():
    """
    Get information about file upload limits and allowed types
    - Public endpoint
    """
    return {
        "max_file_size_mb": FileStorage.MAX_FILE_SIZE / 1024 / 1024,
        "allowed_extensions": list(FileStorage.ALLOWED_IMAGE_EXTENSIONS),
        "thumbnail_size": FileStorage.THUMBNAIL_SIZE
    }

