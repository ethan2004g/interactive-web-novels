"""
Seed script for default chapter templates
Run this to populate the database with default public templates
"""
import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.base import Base  # Import to ensure all models are registered
from app.models.user import User, UserRole
from app.models.chapter_template import ChapterTemplate
from app.utils.default_templates import get_default_templates
from app.core.security import get_password_hash


def create_system_user(db: Session) -> User:
    """
    Create or get a system user for default templates
    """
    system_username = "system_templates"
    
    # Check if system user already exists
    system_user = db.query(User).filter(User.username == system_username).first()
    
    if system_user:
        print(f"+ System user '{system_username}' already exists")
        return system_user
    
    # Create system user
    system_user = User(
        username=system_username,
        email="system@interactivenovels.com",
        password_hash=get_password_hash("system_password_not_used"),
        role=UserRole.AUTHOR,
        bio="System account for default templates"
    )
    
    db.add(system_user)
    db.commit()
    db.refresh(system_user)
    
    print(f"+ Created system user '{system_username}'")
    return system_user


def seed_default_templates(db: Session):
    """
    Seed the database with default chapter templates
    """
    print("Starting template seeding...")
    
    # Get or create system user
    system_user = create_system_user(db)
    
    # Get default templates
    default_templates = get_default_templates()
    
    created_count = 0
    skipped_count = 0
    
    for template_data in default_templates:
        # Check if template already exists
        existing = db.query(ChapterTemplate).filter(
            ChapterTemplate.name == template_data["name"],
            ChapterTemplate.created_by == system_user.id
        ).first()
        
        if existing:
            print(f"- Skipped '{template_data['name']}' (already exists)")
            skipped_count += 1
            continue
        
        # Create new template
        new_template = ChapterTemplate(
            name=template_data["name"],
            description=template_data["description"],
            template_data=template_data["template_data"],
            is_public=template_data["is_public"],
            created_by=system_user.id
        )
        
        db.add(new_template)
        created_count += 1
        print(f"+ Created template '{template_data['name']}'")
    
    db.commit()
    
    print(f"\n{'='*50}")
    print(f"Template seeding complete!")
    print(f"Created: {created_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Total: {len(default_templates)}")
    print(f"{'='*50}")


def main():
    """Main function"""
    print("="*50)
    print("Chapter Template Seeding Script")
    print("="*50)
    print()
    
    db = SessionLocal()
    
    try:
        seed_default_templates(db)
    except Exception as e:
        print(f"\nError during seeding: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()

