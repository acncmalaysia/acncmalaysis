from sqlalchemy import Column, String, DateTime, Float, Text, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from app.core.database import Base

class MissionaryFund(Base):
    __tablename__ = "missionary_funds"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    goal_amount = Column(Float)
    current_amount = Column(Float, default=0)
    currency = Column(String(3), default="MYR")
    status = Column(String(20), default="active")  # active, completed, paused
    image_url = Column(String(500))
    beneficiary_name = Column(String(255))
    beneficiary_country = Column(String(100))
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    donor_count = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<MissionaryFund {self.name}>"
