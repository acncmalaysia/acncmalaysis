from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.core.database import get_db
from app.schemas.fund import FundCreate, FundResponse
from app.models.fund import MissionaryFund
from app.services.fund_service import FundService
from app.services.auth_service import AuthService
from app.models.user import UserRole

router = APIRouter()
fund_service = FundService()
auth_service = AuthService()

@router.post("/", response_model=FundResponse)
async def create_fund(
    fund_data: FundCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth_service.get_current_user)
):
    """Create a new missionary fund (admin only)"""
    if current_user["role"] != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    fund = await fund_service.create_fund(fund_data, db)
    return fund

@router.get("/")
async def get_all_funds(
    status: str = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get all funds"""
    funds = db.query(MissionaryFund).offset(skip).limit(limit).all()
    return funds

@router.get("/featured")
async def get_featured_funds(db: Session = Depends(get_db)):
    """Get featured funds"""
    funds = await fund_service.get_featured_funds(db)
    return funds

@router.get("/{fund_id}", response_model=FundResponse)
async def get_fund(fund_id: UUID, db: Session = Depends(get_db)):
    """Get fund details"""
    fund = await fund_service.get_fund(fund_id, db)
    if not fund:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fund not found"
        )
    return fund

@router.get("/{fund_id}/progress")
async def get_fund_progress(fund_id: UUID, db: Session = Depends(get_db)):
    """Get fund progress"""
    progress = await fund_service.get_fund_progress(fund_id, db)
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fund not found"
        )
    return progress

@router.put("/{fund_id}")
async def update_fund(
    fund_id: UUID,
    fund_data: dict,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth_service.get_current_user)
):
    """Update fund (admin only)"""
    if current_user["role"] != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    fund = await fund_service.update_fund(fund_id, fund_data, db)
    if not fund:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fund not found"
        )
    return fund
