from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.models.user import User
from app.services.auth_service import AuthService

router = APIRouter()
auth_service = AuthService()

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user (donor)"""
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already registered"
        )
    
    user = await auth_service.create_user(user_data, db)
    return user

@router.post("/login")
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login and get JWT tokens"""
    user = await auth_service.authenticate_user(credentials.email, credentials.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    tokens = auth_service.create_tokens(user.id)
    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "token_type": "bearer",
        "user": UserResponse.model_validate(user)
    }

@router.post("/refresh")
async def refresh_token(request: dict):
    """Refresh access token"""
    refresh_token = request.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token required"
        )
    
    user_id = auth_service.verify_refresh_token(refresh_token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    tokens = auth_service.create_tokens(user_id)
    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "token_type": "bearer"
    }

@router.post("/verify-email")
async def verify_email(email: str, code: str, db: Session = Depends(get_db)):
    """Verify email address"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_verified = True
    db.commit()
    return {"message": "Email verified successfully"}
