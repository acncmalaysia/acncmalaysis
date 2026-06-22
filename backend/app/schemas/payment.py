from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class PaymentMethodResponse(BaseModel):
    id: UUID
    country_code: str
    bank_name: str
    account_holder: str
    currency: str
    is_active: bool
    
    class Config:
        from_attributes = True

class BankTransferResponse(BaseModel):
    id: UUID
    amount: float
    currency: str
    reference_number: str
    qr_code_image: Optional[str]
    instructions: Optional[str]
    expires_at: Optional[datetime]
    
    class Config:
        from_attributes = True
