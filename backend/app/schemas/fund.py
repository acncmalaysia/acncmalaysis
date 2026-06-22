from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class FundCreate(BaseModel):
    name: str
    description: str
    goal_amount: float
    currency: str = "MYR"
    beneficiary_name: str
    beneficiary_country: str
    end_date: Optional[datetime] = None

class FundResponse(BaseModel):
    id: UUID
    name: str
    description: str
    goal_amount: float
    current_amount: float
    currency: str
    status: str
    beneficiary_name: str
    beneficiary_country: str
    donor_count: int
    is_featured: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
