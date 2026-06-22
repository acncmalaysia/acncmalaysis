from sqlalchemy import Column, String, DateTime, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from app.core.database import Base
import enum

class UserRole(str, enum.Enum):
    DONOR = "donor"
    ADMIN = "admin"
    STAFF = "staff"

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    phone = Column(String(20))
    role = Column(Enum(UserRole), default=UserRole.DONOR)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    preferred_currency = Column(String(3), default="MYR")
    preferred_language = Column(String(5), default="en")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    
    def __repr__(self):
        return f"<User {self.email}>"
