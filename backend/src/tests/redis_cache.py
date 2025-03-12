import asyncio

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from database.database import async_session
from redis_client import get_redis
from crud.user import (
    select_user_by_email, 
    get_current_auth_user, 
    get_email_from_token,
)
from auth.utils import (
    create_access_token,
    decode_jwt,
)


# Тестовый пользователь
test_user = {"username": "Aleksandr", "email": "rusakov@gmail.com", "password": "test_password"}

# Фикстура для предоставления клиента Redis
@pytest_asyncio.fixture(scope="function")
async def redis_client():
    async for redis in get_redis():
        yield redis
        await redis.aclose()  # Правильное закрытие Redis
        await redis.connection_pool.disconnect()

# Тест без использования кэша
@pytest.mark.asyncio
async def test_get_user_without_cache():
    tasks = []
    for _ in range(10000):
        async def task():
            async with async_session() as session:
                user = await select_user_by_email(email=test_user["email"], session=session)
                assert user is not None  # Проверяем, что пользователь существует
                return user.username

        tasks.append(task())
    results = await asyncio.gather(*tasks)

@pytest.mark.asyncio
async def test_get_cached_user(redis_client: Redis):
    # Создаем список задач
    tasks = []
    for _ in range(10000):  # Количество параллельных запросов
        async def task():
            async with async_session() as session:  # Создаем новую сессию для каждой задачи
                user = await get_current_auth_user(
                    user_email=test_user["email"],
                    session=session,
                    redis_client=redis_client,
                )
                assert user is not None  # Убедитесь, что пользователь существует
                return user.username

        tasks.append(task())
    results = await asyncio.gather(*tasks)

@pytest_asyncio.fixture(scope="function")
async def test_token():
    token = await create_access_token(user_email=test_user["email"])
    return token

@pytest.mark.asyncio
async def test_get_email_from_token(redis_client: Redis):
    test_token = await create_access_token(user_email=test_user["email"])
    payload = decode_jwt(token=test_token)
    expected_email = payload.get("sub")
    uncached_tasks = []
    for _ in range(100):
        async def uncached_task():
            async with async_session() as session:
                email = await get_email_from_token(
                    token=test_token,
                    redis_client=redis_client,
                )
                assert email == expected_email

        uncached_tasks.append(uncached_task())

    tasks = []
    for _ in range(1):
        async def task():
            async with async_session() as session:
                email = await get_email_from_token(
                    token=test_token,
                    redis_client=redis_client,
                )
                assert email == expected_email  # Убедитесь, что пользователь существует

        tasks.append(task())
    await asyncio.gather(*uncached_tasks)
    await asyncio.gather(*tasks)