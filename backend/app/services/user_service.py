"""
User service layer - Business logic for user operations
"""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get user by username"""
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user_in: UserCreate) -> User:
    """Create a new user"""
    # Check if user already exists
    if get_user_by_email(db, user_in.email):
        raise ValueError("Email already registered")
    
    if get_user_by_username(db, user_in.username):
        raise ValueError("Username already taken")
    
    # Create user with hashed password
    db_user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        role=user_in.role,
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: User, user_update: UserUpdate) -> User:
    """Update user profile"""
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Check if username is being changed and if it's available
    if "username" in update_data and update_data["username"] != user.username:
        existing_user = get_user_by_username(db, update_data["username"])
        if existing_user:
            raise ValueError("Username already taken")
    
    # Check if email is being changed and if it's available
    if "email" in update_data and update_data["email"] != user.email:
        existing_user = get_user_by_email(db, update_data["email"])
        if existing_user:
            raise ValueError("Email already registered")
    
    # Update user fields
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, username_or_email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by username/email and password
    Returns user if authentication successful, None otherwise
    """
    # Try to find user by username or email
    user = get_user_by_username(db, username_or_email)
    if not user:
        user = get_user_by_email(db, username_or_email)
    
    if not user:
        return None
    
    if not verify_password(password, user.password_hash):
        return None
    
    return user


def change_password(db: Session, user: User, old_password: str, new_password: str) -> bool:
    """
    Change user password
    Returns True if successful, raises ValueError otherwise
    """
    # Verify old password
    if not verify_password(old_password, user.password_hash):
        raise ValueError("Incorrect password")
    
    # Update password
    user.password_hash = get_password_hash(new_password)
    db.commit()
    return True

