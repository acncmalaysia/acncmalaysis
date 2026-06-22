from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID
from datetime import datetime
from app.models.donation import Donation, DonationStatus
from app.models.fund import MissionaryFund
from app.schemas.donation import DonationCreate
import uuid

class DonationService:
    @staticmethod
    async def create_donation(
        donor_id: UUID,
        donation_data: DonationCreate,
        db: Session
    ) -> Donation:
        """Create a new donation"""
        reference_number = f"DON-{uuid.uuid4().hex[:12].upper()}"
        
        donation = Donation(
            donor_id=donor_id,
            fund_id=donation_data.fund_id,
            amount=donation_data.amount,
            currency=donation_data.currency,
            status=DonationStatus.PENDING,
            payment_method=donation_data.payment_method,
            reference_number=reference_number,
            notes=donation_data.notes,
            anonymous=donation_data.anonymous
        )
        
        db.add(donation)
        db.commit()
        db.refresh(donation)
        return donation
    
    @staticmethod
    async def get_donation(donation_id: UUID, db: Session) -> Donation:
        """Get donation by ID"""
        return db.query(Donation).filter(Donation.id == donation_id).first()
    
    @staticmethod
    async def get_user_donations(donor_id: UUID, db: Session) -> list:
        """Get all donations for a user"""
        return db.query(Donation).filter(Donation.donor_id == donor_id).all()
    
    @staticmethod
    async def complete_donation(donation_id: UUID, db: Session) -> Donation:
        """Mark donation as completed"""
        donation = db.query(Donation).filter(Donation.id == donation_id).first()
        if donation:
            donation.status = DonationStatus.COMPLETED
            donation.completed_at = datetime.utcnow()
            
            # Update fund current amount
            fund = db.query(MissionaryFund).filter(MissionaryFund.id == donation.fund_id).first()
            if fund:
                fund.current_amount += donation.amount
                fund.donor_count += 1
            
            db.commit()
            db.refresh(donation)
        return donation
    
    @staticmethod
    async def cancel_donation(donation_id: UUID, db: Session) -> Donation:
        """Cancel a donation"""
        donation = db.query(Donation).filter(Donation.id == donation_id).first()
        if donation and donation.status == DonationStatus.PENDING:
            donation.status = DonationStatus.CANCELLED
            db.commit()
            db.refresh(donation)
        return donation
    
    @staticmethod
    async def get_donation_stats(db: Session) -> dict:
        """Get donation statistics"""
        total_donations = db.query(func.count(Donation.id)).scalar() or 0
        total_amount = db.query(func.sum(Donation.amount)).scalar() or 0
        completed_donations = db.query(func.count(Donation.id)).filter(
            Donation.status == DonationStatus.COMPLETED
        ).scalar() or 0
        
        return {
            "total_donations": total_donations,
            "total_amount": total_amount,
            "completed_donations": completed_donations,
            "pending_donations": total_donations - completed_donations
        }
