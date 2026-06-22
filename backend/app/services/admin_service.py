from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID
from app.models.user import User, UserRole
from app.models.donation import Donation, DonationStatus
from app.models.fund import MissionaryFund
from datetime import datetime

class AdminService:
    @staticmethod
    async def get_dashboard_stats(db: Session) -> dict:
        """Get admin dashboard statistics"""
        total_users = db.query(func.count(User.id)).scalar() or 0
        total_donors = db.query(func.count(User.id)).filter(
            User.role == UserRole.DONOR
        ).scalar() or 0
        total_staff = db.query(func.count(User.id)).filter(
            User.role == UserRole.STAFF
        ).scalar() or 0
        
        total_donations = db.query(func.count(Donation.id)).scalar() or 0
        total_amount = db.query(func.sum(Donation.amount)).scalar() or 0
        completed_donations = db.query(func.count(Donation.id)).filter(
            Donation.status == DonationStatus.COMPLETED
        ).scalar() or 0
        pending_donations = db.query(func.count(Donation.id)).filter(
            Donation.status == DonationStatus.PENDING
        ).scalar() or 0
        
        active_funds = db.query(func.count(MissionaryFund.id)).filter(
            MissionaryFund.status == "active"
        ).scalar() or 0
        
        return {
            "users": {
                "total": total_users,
                "donors": total_donors,
                "staff": total_staff
            },
            "donations": {
                "total": total_donations,
                "total_amount": total_amount,
                "completed": completed_donations,
                "pending": pending_donations
            },
            "funds": {
                "active": active_funds
            }
        }
    
    @staticmethod
    async def get_all_donations(db: Session, status: str = None, limit: int = 50, offset: int = 0) -> list:
        """Get all donations with optional filtering"""
        query = db.query(Donation)
        if status:
            query = query.filter(Donation.status == status)
        return query.limit(limit).offset(offset).all()
    
    @staticmethod
    async def get_all_users(db: Session, role: str = None, limit: int = 50, offset: int = 0) -> list:
        """Get all users with optional filtering"""
        query = db.query(User)
        if role:
            query = query.filter(User.role == role)
        return query.limit(limit).offset(offset).all()
    
    @staticmethod
    async def update_user_role(user_id: UUID, new_role: UserRole, db: Session) -> User:
        """Update user role"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.role = new_role
            db.commit()
            db.refresh(user)
        return user
    
    @staticmethod
    async def deactivate_user(user_id: UUID, db: Session) -> User:
        """Deactivate user account"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.is_active = False
            db.commit()
            db.refresh(user)
        return user
    
    @staticmethod
    async def get_revenue_report(db: Session, start_date: datetime = None, end_date: datetime = None) -> dict:
        """Get revenue report for date range"""
        query = db.query(
            Donation.currency,
            func.sum(Donation.amount).label('total'),
            func.count(Donation.id).label('count')
        ).filter(Donation.status == DonationStatus.COMPLETED)
        
        if start_date:
            query = query.filter(Donation.completed_at >= start_date)
        if end_date:
            query = query.filter(Donation.completed_at <= end_date)
        
        results = query.group_by(Donation.currency).all()
        
        report = {}
        for currency, total, count in results:
            report[currency] = {"total": total, "count": count}
        
        return report
