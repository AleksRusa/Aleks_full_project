import os

import redis.asyncio as redis

from config.config import settings

redis_url = os.environ.get('REDIS_URL')

async def get_redis():
    redis_client = await redis.from_url(url=redis_url)
    try:
        yield redis_client
    finally:
        await redis_client.aclose()