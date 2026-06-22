from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.models.user import User, UserRole
from app.schemas.user import UserCreate
from uuid import UUID

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    async def create_user(user_data: UserCreate, db: Session) -> User:
        """Create new user account"""
        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=AuthService.hash_password(user_data.password),
            full_name=user_data.full_name,
            phone=user_data.phone,
            preferred_currency=user_data.preferred_currency,
            preferred_language=user_data.preferred_language
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    async def authenticate_user(email: str, password: str, db: Session) -> Optional[User]:
        """Authenticate user with email and password"""
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not AuthService.verify_password(password, user.hashed_password):
            return None
        user.last_login = datetime.utcnow()
        db.commit()
        return user
    
    @staticmethod
    def create_tokens(user_id: UUID) -> dict:
        """Create JWT access and refresh tokens"""
        access_token_expires = timedelta(hours=settings.JWT_EXPIRATION_HOURS)
        refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRATION_DAYS)
        
        access_payload = {
            "sub": str(user_id),
            "exp": datetime.utcnow() + access_token_expires,
            "type": "access"
        }
        refresh_payload = {
            "sub": str(user_id),
            "exp": datetime.utcnow() + refresh_token_expires,
            "type": "refresh"
        }
        
        access_token = jwt.encode(
            access_payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        refresh_token = jwt.encode(
            refresh_payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    
    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except JWTError:
            return None
    
    @staticmethod
    def verify_refresh_token(token: str) -> Optional[str]:
        """Verify refresh token and return user_id"""
        payload = AuthService.verify_token(token)
        if payload and payload.get("type") == "refresh":
            return payload.get("sub")
        return None
    
    @staticmethod
    async def get_current_user(credentials: HTTPAuthCredentials = Depends(security), db: Session = Depends(None)) -> dict:
        """Get current authenticated user from token"""
        token = credentials.credentials
        payload = AuthService.verify_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        return {"user_id": UUID(user_id), "role": UserRole.DONOR}
