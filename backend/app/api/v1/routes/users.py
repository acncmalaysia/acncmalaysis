from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserResponse
from app.models.user import User
from app.services.auth_service import AuthService

router = APIRouter()
auth_service = AuthService()

@router.get("/profile", response_model=UserResponse)
async def get_profile(
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth_service.get_current_user)
):
    """Get current user profile"""
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/profile")
async def update_profile(
    update_data: dict,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth_service.get_current_user)
):
    """Update user profile"""
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Allow only specific fields to be updated
    allowed_fields = ["full_name", "phone", "preferred_currency", "preferred_language"]
    for key, value in update_data.items():
        if key in allowed_fields:
            setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return {"message": "Profile updated successfully", "user": UserResponse.model_validate(user)}

@router.get("/")
async def list_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """List all users (public info only)"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users
