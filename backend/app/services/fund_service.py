from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID
from datetime import datetime
from app.models.fund import MissionaryFund
from app.schemas.fund import FundCreate

class FundService:
    @staticmethod
    async def create_fund(fund_data: FundCreate, db: Session) -> MissionaryFund:
        """Create a new missionary fund"""
        fund = MissionaryFund(
            name=fund_data.name,
            description=fund_data.description,
            goal_amount=fund_data.goal_amount,
            currency=fund_data.currency,
            beneficiary_name=fund_data.beneficiary_name,
            beneficiary_country=fund_data.beneficiary_country,
            end_date=fund_data.end_date
        )
        db.add(fund)
        db.commit()
        db.refresh(fund)
        return fund
    
    @staticmethod
    async def get_fund(fund_id: UUID, db: Session) -> MissionaryFund:
        """Get fund by ID"""
        return db.query(MissionaryFund).filter(MissionaryFund.id == fund_id).first()
    
    @staticmethod
    async def get_all_funds(db: Session, status: str = "active") -> list:
        """Get all funds or filtered by status"""
        query = db.query(MissionaryFund)
        if status:
            query = query.filter(MissionaryFund.status == status)
        return query.all()
    
    @staticmethod
    async def get_featured_funds(db: Session, limit: int = 5) -> list:
        """Get featured funds"""
        return db.query(MissionaryFund).filter(
            MissionaryFund.is_featured == True,
            MissionaryFund.status == "active"
        ).limit(limit).all()
    
    @staticmethod
    async def update_fund(fund_id: UUID, fund_data: dict, db: Session) -> MissionaryFund:
        """Update fund details"""
        fund = db.query(MissionaryFund).filter(MissionaryFund.id == fund_id).first()
        if fund:
            for key, value in fund_data.items():
                if hasattr(fund, key) and key != "id":
                    setattr(fund, key, value)
            fund.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(fund)
        return fund
    
    @staticmethod
    async def get_fund_progress(fund_id: UUID, db: Session) -> dict:
        """Get fund progress percentage"""
        fund = db.query(MissionaryFund).filter(MissionaryFund.id == fund_id).first()
        if fund and fund.goal_amount:
            progress = (fund.current_amount / fund.goal_amount) * 100
            return {
                "fund_id": fund_id,
                "current_amount": fund.current_amount,
                "goal_amount": fund.goal_amount,
                "progress_percentage": min(progress, 100),
                "donor_count": fund.donor_count
            }
        return None
