import os
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from app.models.donation import DonationReceipt
from app.core.config import get_settings

settings = get_settings()

class FileService:
    @staticmethod
    def allowed_file(filename: str) -> bool:
        """Check if file extension is allowed"""
        allowed_extensions = settings.ALLOWED_EXTENSIONS
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
    
    @staticmethod
    def validate_file_size(file_size: int) -> bool:
        """Check if file size is within limit"""
        return file_size <= settings.MAX_UPLOAD_SIZE
    
    @staticmethod
    async def save_receipt_file(
        file_content: bytes,
        file_name: str,
        donation_id: str,
        db: Session
    ) -> DonationReceipt:
        """Save donation receipt file"""
        # Generate unique filename
        file_extension = file_name.rsplit('.', 1)[1].lower()
        unique_filename = f"receipt_{donation_id}_{uuid.uuid4().hex}.{file_extension}"
        
        # Create uploads directory if it doesn't exist
        upload_dir = "uploads/receipts"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save file
        file_path = os.path.join(upload_dir, unique_filename)
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        # Create receipt record in database
        receipt = DonationReceipt(
            donation_id=donation_id,
            file_path=file_path,
            file_type=file_extension,
            file_size=len(file_content),
            uploaded_at=datetime.utcnow()
        )
        db.add(receipt)
        db.commit()
        db.refresh(receipt)
        return receipt
    
    @staticmethod
    async def delete_receipt_file(receipt_id: str, db: Session) -> bool:
        """Delete receipt file"""
        receipt = db.query(DonationReceipt).filter(DonationReceipt.id == receipt_id).first()
        if receipt and receipt.file_path:
            try:
                if os.path.exists(receipt.file_path):
                    os.remove(receipt.file_path)
                db.delete(receipt)
                db.commit()
                return True
            except Exception as e:
                print(f"Error deleting file: {e}")
                return False
        return False
    
    @staticmethod
    async def verify_receipt(receipt_id: str, verified_by_id: str, db: Session) -> DonationReceipt:
        """Verify receipt by admin"""
        receipt = db.query(DonationReceipt).filter(DonationReceipt.id == receipt_id).first()
        if receipt:
            receipt.verified = True
            receipt.verified_at = datetime.utcnow()
            receipt.verified_by = verified_by_id
            db.commit()
            db.refresh(receipt)
        return receipt
