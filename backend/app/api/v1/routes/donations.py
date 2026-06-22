from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from uuid import UUID
from app.core.database import get_db
from app.schemas.donation import DonationCreate, DonationResponse
from app.models.donation import Donation
from app.services.auth_service import AuthService
from app.services.donation_service import DonationService
from app.services.file_service import FileService

router = APIRouter()
auth_service = AuthService()
donation_service = DonationService()
file_service = FileService()

@router.post("/", response_model=DonationResponse)
async def create_donation(
    donation_data: DonationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth_service.get_current_user)
):
    """Create a new donation"""
    donation = await donation_service.create_donation(
        donor_id=current_user["user_id"],
        donation_data=donation_data,
        db=db
    )
    return donation

@router.get("/{donation_id}", response_model=DonationResponse)
async def get_donation(
    donation_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth_service.get_current_user)
):
    """Get donation details"""
    donation = await donation_service.get_donation(donation_id, db)
    if not donation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donation not found"
        )
    # Check ownership or admin access
    if donation.donor_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this donation"
        )
    return donation

@router.get("/")
async def get_my_donations(
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth_service.get_current_user)
):
    """Get current user's donations"""
    donations = await donation_service.get_user_donations(current_user["user_id"], db)
    return donations

@router.post("/{donation_id}/upload-receipt")
async def upload_receipt(
    donation_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth_service.get_current_user)
):
    """Upload donation receipt"""
    donation = await donation_service.get_donation(donation_id, db)
    if not donation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donation not found"
        )
    
    if donation.donor_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to upload receipt for this donation"
        )
    
    if not file_service.allowed_file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File type not allowed. Allowed types: pdf, jpg, jpeg, png"
        )
    
    content = await file.read()
    if not file_service.validate_file_size(len(content)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds maximum limit (5MB)"
        )
    
    receipt = await file_service.save_receipt_file(content, file.filename, str(donation_id), db)
    return {"message": "Receipt uploaded successfully", "receipt_id": str(receipt.id)}

@router.get("/{donation_id}/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get donation statistics"""
    stats = await donation_service.get_donation_stats(db)
    return stats
