import redis.asyncio as redis
from app.core.config import settings
from typing import Optional

class RedisConnection:
    def __init__(self):
        self._redis: Optional[redis.Redis] = None
    
    async def connect(self) -> redis.Redis:
        if self._redis is None:
            self._redis = redis.from_url(
                settings.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
        return self._redis
    
    async def disconnect(self):
        if self._redis:
            await self._redis.close()
            self._redis = None
    
    async def get_client(self) -> redis.Redis:
        return await self.connect()

redis_connection = RedisConnection()

async def get_redis() -> redis.Redis:
    return await redis_connection.get_client()