from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from redis.asyncio import Redis
import os
from models.db import AsyncSessionLocal, engine

router = APIRouter()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

@router.get("/health")
async def health_check():
    # Check DB
    try:
        async with AsyncSessionLocal() as session:
            await session.execute("SELECT 1")
        db_status = "ok"
    except SQLAlchemyError:
        db_status = "error"
    # Check Redis
    try:
        redis = Redis.from_url(REDIS_URL)
        await redis.ping()
        redis_status = "ok"
    except Exception:
        redis_status = "error"
    return {"db": db_status, "redis": redis_status}
