"""
User profile endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.user import User as UserSchema, UserUpdate, UserPasswordUpdate
from app.services import user_service

router = APIRouter()


@router.get("/me", response_model=UserSchema)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user's profile
    
    Requires authentication
    """
    return current_user


@router.put("/me", response_model=UserSchema)
def update_my_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user's profile
    
    Requires authentication
    
    - **username**: New username (optional)
    - **email**: New email (optional)
    - **bio**: User bio (optional)
    - **profile_picture_url**: Profile picture URL (optional)
    """
    try:
        updated_user = user_service.update_user(db, current_user, user_update)
        return updated_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/me/password")
def change_my_password(
    password_update: UserPasswordUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change current user's password
    
    Requires authentication
    
    - **old_password**: Current password
    - **new_password**: New password (minimum 8 characters)
    """
    try:
        user_service.change_password(
            db,
            current_user,
            password_update.old_password,
            password_update.new_password
        )
        return {"message": "Password changed successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{user_id}", response_model=UserSchema)
def get_user_profile(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get public profile of any user by ID
    
    Does not require authentication
    """
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.get("/username/{username}", response_model=UserSchema)
def get_user_by_username(
    username: str,
    db: Session = Depends(get_db)
):
    """
    Get public profile of any user by username
    
    Does not require authentication
    """
    user = user_service.get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

