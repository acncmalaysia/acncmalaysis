from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: str
    phone: Optional[str] = None
    preferred_currency: str = "MYR"
    preferred_language: str = "en"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    email: str
    username: str
    full_name: str
    phone: Optional[str]
    role: str
    is_active: bool
    preferred_currency: str
    preferred_language: str
    created_at: datetime
    
    class Config:
        from_attributes = True
