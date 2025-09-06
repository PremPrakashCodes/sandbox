from fastapi import APIRouter
from app.core.config import settings
from app.core.redis import get_redis
from app.core.database import async_engine
from sqlalchemy import text

router = APIRouter()

@router.get("/")
async def get_root():
    return {"message": "Sandbox API", "version": settings.version}

@router.get("/health")
async def health_check():
    # Test Redis connection
    try:
        redis_client = await get_redis()
        await redis_client.ping()
        redis_status = "connected"
    except Exception as e:
        redis_status = f"error: {str(e)}"

    # Test database connection
    try:
        async with async_engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        postgres_status = "connected"
    except Exception as e:
        postgres_status = f"error: {str(e)}"

    return {
        "status": "healthy", 
        "version": settings.version,
        "redis": redis_status,
        "database": postgres_status
    }