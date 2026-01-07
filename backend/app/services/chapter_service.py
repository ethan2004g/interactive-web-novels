"""
Chapter service layer - Business logic for chapter operations
"""
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from datetime import datetime
from app.models.chapter import Chapter, ContentType
from app.models.book import Book
from app.models.user import User
from app.schemas.chapter import ChapterCreate, ChapterUpdate


def get_chapter_by_id(db: Session, chapter_id: int) -> Optional[Chapter]:
    """Get chapter by ID"""
    return db.query(Chapter).filter(Chapter.id == chapter_id).first()


def get_chapters_by_book(
    db: Session,
    book_id: int,
    published_only: bool = False
) -> List[Chapter]:
    """
    Get all chapters for a specific book
    Returns chapters ordered by chapter_number
    """
    query = db.query(Chapter).filter(Chapter.book_id == book_id)
    
    if published_only:
        query = query.filter(Chapter.is_published == True)
    
    return query.order_by(Chapter.chapter_number).all()


def create_chapter(db: Session, chapter_in: ChapterCreate, book_id: int) -> Chapter:
    """Create a new chapter"""
    # Calculate word count
    word_count = calculate_word_count(chapter_in.content_data, chapter_in.content_type)
    
    # Set published_at if chapter is published
    published_at = None
    if chapter_in.is_published:
        published_at = datetime.utcnow()
    
    db_chapter = Chapter(
        **chapter_in.model_dump(),
        book_id=book_id,
        word_count=word_count,
        published_at=published_at
    )
    
    db.add(db_chapter)
    db.commit()
    db.refresh(db_chapter)
    return db_chapter


def update_chapter(db: Session, chapter: Chapter, chapter_update: ChapterUpdate) -> Chapter:
    """Update a chapter"""
    update_data = chapter_update.model_dump(exclude_unset=True)
    
    # If content is updated, recalculate word count
    if 'content_data' in update_data or 'content_type' in update_data:
        content_data = update_data.get('content_data', chapter.content_data)
        content_type = update_data.get('content_type', chapter.content_type)
        update_data['word_count'] = calculate_word_count(content_data, content_type)
    
    # If is_published is being set to True and wasn't published before, set published_at
    if 'is_published' in update_data and update_data['is_published'] and not chapter.is_published:
        update_data['published_at'] = datetime.utcnow()
    
    # If is_published is being set to False, clear published_at
    if 'is_published' in update_data and not update_data['is_published'] and chapter.is_published:
        update_data['published_at'] = None
    
    for field, value in update_data.items():
        setattr(chapter, field, value)
    
    db.commit()
    db.refresh(chapter)
    return chapter


def delete_chapter(db: Session, chapter: Chapter) -> bool:
    """Delete a chapter"""
    db.delete(chapter)
    db.commit()
    return True


def reorder_chapters(db: Session, book_id: int, chapter_id: int, new_chapter_number: int) -> List[Chapter]:
    """
    Reorder chapters within a book
    Moves chapter to new position and adjusts other chapter numbers accordingly
    """
    # Get the chapter to move
    chapter = db.query(Chapter).filter(
        Chapter.id == chapter_id,
        Chapter.book_id == book_id
    ).first()
    
    if not chapter:
        return []
    
    old_number = chapter.chapter_number
    
    # Get all chapters for this book
    all_chapters = db.query(Chapter).filter(
        Chapter.book_id == book_id
    ).order_by(Chapter.chapter_number).all()
    
    # Validate new_chapter_number
    if new_chapter_number < 1 or new_chapter_number > len(all_chapters):
        return []
    
    if old_number == new_chapter_number:
        # No change needed
        return all_chapters
    
    # Remove chapter from list
    all_chapters.remove(chapter)
    
    # Insert at new position (new_chapter_number is 1-indexed)
    all_chapters.insert(new_chapter_number - 1, chapter)
    
    # To avoid unique constraint violations, first set all chapter_numbers to negative values
    for idx, chap in enumerate(all_chapters, start=1):
        chap.chapter_number = -(idx + 1000)  # Use negative numbers temporarily
    
    db.flush()  # Flush the negative numbers
    
    # Now set the correct chapter_numbers
    for idx, chap in enumerate(all_chapters, start=1):
        chap.chapter_number = idx
    
    db.commit()
    
    # Refresh all chapters
    for chap in all_chapters:
        db.refresh(chap)
    
    return all_chapters


def calculate_word_count(content_data: dict, content_type: ContentType) -> int:
    """Calculate word count from content_data"""
    if content_type == ContentType.SIMPLE:
        text = content_data.get('text', '')
        return len(text.split())
    elif content_type == ContentType.INTERACTIVE:
        # For interactive content, count words in all text nodes
        total_words = 0
        nodes = content_data.get('nodes', [])
        for node in nodes:
            if isinstance(node, dict):
                # Count words in various text fields
                if 'text' in node:
                    total_words += len(str(node['text']).split())
                if 'content' in node:
                    total_words += len(str(node['content']).split())
                if 'dialogue' in node:
                    total_words += len(str(node['dialogue']).split())
        return total_words
    return 0


def get_book_by_chapter(db: Session, chapter_id: int) -> Optional[Book]:
    """Get the book that a chapter belongs to"""
    chapter = get_chapter_by_id(db, chapter_id)
    if chapter:
        return db.query(Book).filter(Book.id == chapter.book_id).first()
    return None


def is_chapter_author(db: Session, chapter: Chapter, user: User) -> bool:
    """Check if user is the author of the book that this chapter belongs to"""
    book = db.query(Book).filter(Book.id == chapter.book_id).first()
    if book:
        return book.author_id == user.id
    return False


def get_next_chapter_number(db: Session, book_id: int) -> int:
    """Get the next available chapter number for a book"""
    max_number = db.query(func.max(Chapter.chapter_number)).filter(
        Chapter.book_id == book_id
    ).scalar()
    
    return (max_number or 0) + 1

