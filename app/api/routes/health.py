from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "JustHomes AI API",
        "timestamp": datetime.utcnow().isoformat(),
    }