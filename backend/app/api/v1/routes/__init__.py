from fastapi import APIRouter
from app.api.v1.routes import auth, donations, funds, users, admin

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(donations.router, prefix="/donations", tags=["Donations"])
router.include_router(funds.router, prefix="/funds", tags=["Funds"])
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(admin.router, prefix="/admin", tags=["Admin"])
