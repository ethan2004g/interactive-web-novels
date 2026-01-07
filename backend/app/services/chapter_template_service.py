"""
Chapter Template service layer - Business logic for chapter template operations
"""
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from app.models.chapter_template import ChapterTemplate
from app.models.user import User
from app.schemas.chapter_template import ChapterTemplateCreate, ChapterTemplateUpdate


def get_template_by_id(db: Session, template_id: int) -> Optional[ChapterTemplate]:
    """Get chapter template by ID"""
    return db.query(ChapterTemplate).filter(ChapterTemplate.id == template_id).first()


def get_templates(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    user_id: Optional[int] = None,
    public_only: bool = False,
    search_query: Optional[str] = None
) -> Tuple[List[ChapterTemplate], int]:
    """
    Get chapter templates with filters
    
    Args:
        db: Database session
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
        user_id: If provided, returns only templates created by this user OR public templates
        public_only: If True, returns only public templates
        search_query: Search term for template name or description
    
    Returns:
        Tuple of (list of templates, total count)
    """
    query = db.query(ChapterTemplate)
    
    # Apply filters
    filters = []
    
    if user_id and not public_only:
        # Return templates created by user OR public templates
        filters.append(
            or_(
                ChapterTemplate.created_by == user_id,
                ChapterTemplate.is_public == True
            )
        )
    elif public_only:
        # Return only public templates
        filters.append(ChapterTemplate.is_public == True)
    
    if search_query:
        search_term = f"%{search_query}%"
        filters.append(
            or_(
                ChapterTemplate.name.ilike(search_term),
                ChapterTemplate.description.ilike(search_term)
            )
        )
    
    if filters:
        query = query.filter(and_(*filters))
    
    # Get total count
    total = query.count()
    
    # Apply pagination and ordering
    templates = query.order_by(ChapterTemplate.created_at.desc()).offset(skip).limit(limit).all()
    
    return templates, total


def get_templates_by_user(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 20
) -> Tuple[List[ChapterTemplate], int]:
    """Get all templates created by a specific user"""
    query = db.query(ChapterTemplate).filter(ChapterTemplate.created_by == user_id)
    
    total = query.count()
    templates = query.order_by(ChapterTemplate.created_at.desc()).offset(skip).limit(limit).all()
    
    return templates, total


def get_public_templates(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    search_query: Optional[str] = None
) -> Tuple[List[ChapterTemplate], int]:
    """Get all public templates"""
    return get_templates(db, skip=skip, limit=limit, public_only=True, search_query=search_query)


def get_popular_templates(
    db: Session,
    limit: int = 10
) -> List[ChapterTemplate]:
    """Get most popular public templates (by usage count)"""
    return db.query(ChapterTemplate).filter(
        ChapterTemplate.is_public == True
    ).order_by(
        ChapterTemplate.usage_count.desc()
    ).limit(limit).all()


def create_template(db: Session, template_in: ChapterTemplateCreate, user_id: int) -> ChapterTemplate:
    """Create a new chapter template"""
    db_template = ChapterTemplate(
        **template_in.model_dump(),
        created_by=user_id
    )
    
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template


def update_template(
    db: Session,
    template: ChapterTemplate,
    template_update: ChapterTemplateUpdate
) -> ChapterTemplate:
    """Update a chapter template"""
    update_data = template_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(template, field, value)
    
    db.commit()
    db.refresh(template)
    return template


def delete_template(db: Session, template: ChapterTemplate) -> bool:
    """Delete a chapter template"""
    db.delete(template)
    db.commit()
    return True


def increment_usage_count(db: Session, template: ChapterTemplate) -> ChapterTemplate:
    """Increment the usage count of a template"""
    template.usage_count += 1
    db.commit()
    db.refresh(template)
    return template


def is_template_owner(template: ChapterTemplate, user: User) -> bool:
    """Check if user is the owner of the template"""
    return template.created_by == user.id


def can_view_template(template: ChapterTemplate, user: Optional[User] = None) -> bool:
    """Check if user can view the template (public OR owned by user)"""
    if template.is_public:
        return True
    if user and template.created_by == user.id:
        return True
    return False


def can_edit_template(template: ChapterTemplate, user: User) -> bool:
    """Check if user can edit the template (must be owner)"""
    return is_template_owner(template, user)

