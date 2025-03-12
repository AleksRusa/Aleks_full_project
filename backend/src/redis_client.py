import redis.asyncio as redis


async def get_redis():
    redis_client = await redis.from_url("redis://localhost:6379")
    try:
        yield redis_client
    finally:
        await redis_client.aclose()