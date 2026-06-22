from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class DonationCreate(BaseModel):
    fund_id: UUID
    amount: float
    currency: str = "MYR"
    payment_method: str
    notes: Optional[str] = None
    anonymous: bool = False

class DonationResponse(BaseModel):
    id: UUID
    donor_id: UUID
    fund_id: UUID
    amount: float
    currency: str
    status: str
    payment_method: str
    transaction_id: Optional[str]
    reference_number: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class DonationReceiptResponse(BaseModel):
    id: UUID
    donation_id: UUID
    file_path: Optional[str]
    file_type: Optional[str]
    verified: bool
    uploaded_at: datetime
    
    class Config:
        from_attributes = True
