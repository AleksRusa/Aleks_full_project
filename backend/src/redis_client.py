import os

import redis.asyncio as redis

from config.config import settings

REDIS_URL_async = settings.redis_url_aioredis
redis_url = os.environ.get('REDIS_URL') or REDIS_URL_async

async def get_redis():
    redis_client = await redis.from_url(url=redis_url)
    try:
        yield redis_client
    finally:
        await redis_client.aclose()