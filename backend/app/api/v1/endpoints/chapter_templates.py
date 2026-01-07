"""
Chapter Templates endpoints - CRUD operations for chapter templates
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user, get_current_author
from app.models.user import User
from app.schemas.chapter_template import (
    ChapterTemplate, ChapterTemplateCreate, ChapterTemplateUpdate,
    ChapterTemplateSummary, ChapterTemplateListResponse, ChapterTemplateWithCreator
)
from app.services import chapter_template_service

router = APIRouter()


@router.post("/chapter-templates", response_model=ChapterTemplate, status_code=status.HTTP_201_CREATED)
def create_template(
    template_in: ChapterTemplateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_author)
):
    """
    Create a new chapter template (Authors only)
    
    - **name**: Template name (required)
    - **description**: Template description
    - **template_data**: Template structure in JSON format (required)
    - **is_public**: Whether template is publicly available (default: false)
    - **preview_image_url**: URL to preview image
    """
    template = chapter_template_service.create_template(db, template_in, current_user.id)
    return template


@router.get("/chapter-templates", response_model=ChapterTemplateListResponse)
def get_templates(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of records to return"),
    public_only: bool = Query(False, description="Only return public templates"),
    search: Optional[str] = Query(None, description="Search query for template name or description"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Get chapter templates with optional filters
    
    - **skip**: Pagination offset (default: 0)
    - **limit**: Number of templates to return (default: 20, max: 100)
    - **public_only**: If true, only return public templates (default: false)
    - **search**: Search term for template name or description
    
    If authenticated, returns templates created by the user OR public templates.
    If not authenticated or public_only=true, returns only public templates.
    """
    user_id = current_user.id if current_user else None
    
    templates, total = chapter_template_service.get_templates(
        db,
        skip=skip,
        limit=limit,
        user_id=user_id if not public_only else None,
        public_only=public_only,
        search_query=search
    )
    
    return {
        "templates": templates,
        "total": total
    }


@router.get("/chapter-templates/popular", response_model=List[ChapterTemplateSummary])
def get_popular_templates(
    limit: int = Query(10, ge=1, le=50, description="Number of templates to return"),
    db: Session = Depends(get_db)
):
    """
    Get most popular public templates (sorted by usage count)
    
    - **limit**: Number of templates to return (default: 10, max: 50)
    """
    templates = chapter_template_service.get_popular_templates(db, limit=limit)
    return templates


@router.get("/chapter-templates/my-templates", response_model=ChapterTemplateListResponse)
def get_my_templates(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_author)
):
    """
    Get all templates created by the current user (Authors only)
    
    - **skip**: Pagination offset (default: 0)
    - **limit**: Number of templates to return (default: 20, max: 100)
    """
    templates, total = chapter_template_service.get_templates_by_user(
        db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    
    return {
        "templates": templates,
        "total": total
    }


@router.get("/chapter-templates/{template_id}", response_model=ChapterTemplate)
def get_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Get a specific chapter template by ID
    
    - **template_id**: ID of the template
    
    Returns the template if it's public OR if the current user is the owner.
    """
    template = chapter_template_service.get_template_by_id(db, template_id)
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    # Check if user can view this template
    if not chapter_template_service.can_view_template(template, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this template"
        )
    
    return template


@router.put("/chapter-templates/{template_id}", response_model=ChapterTemplate)
def update_template(
    template_id: int,
    template_update: ChapterTemplateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_author)
):
    """
    Update a chapter template (Authors only - must be template owner)
    
    - **template_id**: ID of the template to update
    - **name**: New template name
    - **description**: New template description
    - **template_data**: Updated template structure
    - **is_public**: Change public/private status
    - **preview_image_url**: Updated preview image URL
    """
    template = chapter_template_service.get_template_by_id(db, template_id)
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    # Check if user is the template owner
    if not chapter_template_service.can_edit_template(template, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to edit this template"
        )
    
    updated_template = chapter_template_service.update_template(db, template, template_update)
    return updated_template


@router.delete("/chapter-templates/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_author)
):
    """
    Delete a chapter template (Authors only - must be template owner)
    
    - **template_id**: ID of the template to delete
    """
    template = chapter_template_service.get_template_by_id(db, template_id)
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    # Check if user is the template owner
    if not chapter_template_service.can_edit_template(template, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this template"
        )
    
    chapter_template_service.delete_template(db, template)
    return None


@router.post("/chapter-templates/{template_id}/use", response_model=ChapterTemplate)
def use_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_author)
):
    """
    Mark a template as used (increments usage count)
    
    This endpoint should be called when an author uses this template to create a chapter.
    
    - **template_id**: ID of the template being used
    """
    template = chapter_template_service.get_template_by_id(db, template_id)
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    # Check if user can view this template
    if not chapter_template_service.can_view_template(template, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to use this template"
        )
    
    updated_template = chapter_template_service.increment_usage_count(db, template)
    return updated_template

