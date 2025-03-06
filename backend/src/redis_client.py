import aioredis

from config.config import settings

async def get_redis():
    redis = await aioredis.from_url(settings.redis_url_aioredis)
    try:
        yield redis
    finally:
        await redis.close()