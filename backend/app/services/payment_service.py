import qrcode
import io
import uuid
from typing import Optional
from PIL import Image
from app.core.config import get_settings

settings = get_settings()

class PaymentService:
    @staticmethod
    def generate_qr_code(
        bank_name: str,
        account_number: str,
        amount: float,
        reference: str,
        currency: str = "MYR",
        country: str = "MY"
    ) -> Image.Image:
        """
        Generate QR code for bank transfer
        Supports:
        - Malaysia: DuitNow
        - Hong Kong: FPS (Faster Payment System)
        - Australia: PayID
        """
        qr_data = PaymentService._format_qr_data(
            bank_name, account_number, amount, reference, currency, country
        )
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        return img
    
    @staticmethod
    def _format_qr_data(
        bank_name: str,
        account_number: str,
        amount: float,
        reference: str,
        currency: str,
        country: str
    ) -> str:
        """
        Format QR code data based on country standards
        """
        # Malaysia DuitNow format (EMV QR)
        if country == "MY":
            return f"00020126360014my.co.duitnow0115{account_number}52040000530398450611{amount}5802MY6304"
        
        # Hong Kong FPS format (ISO 20022)
        elif country == "HK":
            return f"00020126480014hk.fps0414{account_number}52040000530398450612{amount}5802HK6304"
        
        # Australia PayID format (AS/NZS 4834)
        elif country == "AU":
            return f"00020126480014au.payid0414{account_number}52040000530398450612{amount}5802AU6304"
        
        # China WeChat Pay / Alipay
        elif country == "CN":
            return f"00020126480014cn.weixin0414{account_number}52040000530398450612{amount}5802CN6304"
        
        # Singapore
        elif country == "SG":
            return f"00020126480014sg.paynow0414{account_number}52040000530398450612{amount}5802SG6304"
        
        # Default generic format
        else:
            return f"{bank_name}|{account_number}|{amount} {currency}|REF: {reference}"
    
    @staticmethod
    def get_payment_instructions(country: str, bank_name: str, amount: float, currency: str) -> str:
        """
        Get human-readable payment instructions based on country
        """
        if country == "MY":
            return f"Please transfer {amount} {currency} to {bank_name}. Scan the QR code or use DuitNow."
        elif country == "HK":
            return f"Please transfer {amount} {currency} to {bank_name}. Use FPS or scan the QR code."
        elif country == "AU":
            return f"Please transfer {amount} {currency} to {bank_name}. Use PayID or scan the QR code."
        elif country == "CN":
            return f"Please transfer {amount} {currency} to {bank_name}. Use WeChat Pay or Alipay."
        elif country == "SG":
            return f"Please transfer {amount} {currency} to {bank_name}. Use PayNow or scan the QR code."
        else:
            return f"Please transfer {amount} {currency} to {bank_name}."
