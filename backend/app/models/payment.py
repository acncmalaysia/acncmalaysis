from sqlalchemy import Column, String, DateTime, Boolean, Float
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from app.core.database import Base

class PaymentMethod(Base):
    __tablename__ = "payment_methods"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    country_code = Column(String(2), nullable=False)  # MY, HK, AU
    bank_name = Column(String(255), nullable=False)
    account_holder = Column(String(255), nullable=False)
    account_number = Column(String(50))
    bank_code = Column(String(10))
    swift_code = Column(String(20))
    currency = Column(String(3), nullable=False)
    qr_code_data = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<PaymentMethod {self.bank_name} - {self.country_code}>"

class BankTransfer(Base):
    __tablename__ = "bank_transfers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    payment_method_id = Column(UUID(as_uuid=True), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False)
    reference_number = Column(String(255), unique=True, index=True)
    qr_code_image = Column(String(500))  # URL to stored QR code image
    instructions = Column(String(1000))
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<BankTransfer {self.reference_number}>"
