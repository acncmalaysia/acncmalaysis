from sqlalchemy import Column, String, DateTime, Boolean, Float, ForeignKey, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from app.core.database import Base
import enum

class DonationStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Donation(Base):
    __tablename__ = "donations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    donor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    fund_id = Column(UUID(as_uuid=True), ForeignKey("missionary_funds.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="MYR")
    status = Column(Enum(DonationStatus), default=DonationStatus.PENDING)
    payment_method = Column(String(50), nullable=False)  # bank_transfer, qr_code, etc.
    transaction_id = Column(String(255), unique=True, index=True)
    reference_number = Column(String(255), unique=True, index=True)
    notes = Column(Text)
    anonymous = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime)
    
    def __repr__(self):
        return f"<Donation {self.id}>"

class DonationReceipt(Base):
    __tablename__ = "donation_receipts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    donation_id = Column(UUID(as_uuid=True), ForeignKey("donations.id"), unique=True, nullable=False)
    file_path = Column(String(500))
    file_type = Column(String(20))  # pdf, jpg, png
    file_size = Column(Float)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    verified = Column(Boolean, default=False)
    verified_at = Column(DateTime)
    verified_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    def __repr__(self):
        return f"<DonationReceipt {self.donation_id}>"
