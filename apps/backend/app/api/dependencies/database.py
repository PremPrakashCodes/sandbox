from app.core.database import get_async_db
from app.core.redis import get_redis

async def get_db_dependency():
    async for db in get_async_db():
        yield db

async def get_redis_dependency():
    return await get_redis()