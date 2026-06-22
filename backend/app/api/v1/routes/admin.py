from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from app.core.database import get_db
from app.models.user import User, UserRole
from app.models.donation import Donation
from app.services.auth_service import AuthService
from app.services.admin_service import AdminService
from app.services.file_service import FileService

router = APIRouter()
auth_service = AuthService()
admin_service = AdminService()
file_service = FileService()

def verify_admin(current_user: dict = Depends(auth_service.get_current_user)) -> dict:
    """Verify user has admin role"""
    if current_user["role"] != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

@router.get("/dashboard")
async def admin_dashboard(
    db: Session = Depends(get_db),
    admin_user: dict = Depends(verify_admin)
):
    """Get admin dashboard statistics"""
    stats = await admin_service.get_dashboard_stats(db)
    return stats

@router.get("/donations")
async def get_all_donations(
    status: str = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    admin_user: dict = Depends(verify_admin)
):
    """Get all donations (admin only)"""
    donations = await admin_service.get_all_donations(db, status, limit, skip)
    return donations

@router.get("/users")
async def get_all_users(
    role: str = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    admin_user: dict = Depends(verify_admin)
):
    """Get all users (admin only)"""
    users = await admin_service.get_all_users(db, role, limit, skip)
    return users

@router.post("/donations/{donation_id}/verify-receipt")
async def verify_receipt(
    donation_id: UUID,
    receipt_id: UUID,
    db: Session = Depends(get_db),
    admin_user: dict = Depends(verify_admin)
):
    """Verify donation receipt (admin only)"""
    receipt = await file_service.verify_receipt(str(receipt_id), str(admin_user["user_id"]), db)
    if not receipt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receipt not found"
        )
    return {"message": "Receipt verified", "receipt_id": str(receipt.id)}

@router.put("/users/{user_id}/role")
async def update_user_role(
    user_id: UUID,
    new_role: str,
    db: Session = Depends(get_db),
    admin_user: dict = Depends(verify_admin)
):
    """Update user role (admin only)"""
    try:
        role = UserRole(new_role)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role"
        )
    
    user = await admin_service.update_user_role(user_id, role, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"message": "User role updated", "user_id": str(user.id), "role": user.role}

@router.post("/users/{user_id}/deactivate")
async def deactivate_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    admin_user: dict = Depends(verify_admin)
):
    """Deactivate user account (admin only)"""
    user = await admin_service.deactivate_user(user_id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"message": "User deactivated", "user_id": str(user.id)}

@router.get("/reports/revenue")
async def get_revenue_report(
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db),
    admin_user: dict = Depends(verify_admin)
):
    """Get revenue report (admin only)"""
    start = datetime.fromisoformat(start_date) if start_date else None
    end = datetime.fromisoformat(end_date) if end_date else None
    
    report = await admin_service.get_revenue_report(db, start, end)
    return report
