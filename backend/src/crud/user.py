import asyncio
import json

from jwt import InvalidTokenError, ExpiredSignatureError
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, values, select, delete
from fastapi import HTTPException, Depends, status, Request, Response
# from fastapi.security import (
#     HTTPBearer, 
#     HTTPAuthorizationCredentials, 
#     OAuth2PasswordBearer,
#     OAuth2PasswordRequestForm,
# )
from pydantic import ValidationError, EmailStr
from redis.asyncio import Redis

from schemas.user import UserInfo, UserLogin, UserSchema, Token, UserPasswd
from auth.utils import (
    validate_password, 
    decode_jwt,
    create_access_token,
    create_refresh_token,
)
from database.models import User
from database.database import get_db
from redis_client import get_redis

async def create_user(
    session: AsyncSession, 
    user_data: UserSchema,
):
    try:
        user_dict = user_data.model_dump(exclude_unset=True)
        user = User(**user_dict)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return f"пользователь {user.username} успешно зарегистрирован"
    except IntegrityError as e:
        # Обработка конфликта уникальности (например, дублирующийся email)
        if "users_email_key" in str(e.orig):
            raise HTTPException(
                status_code=409,  # Conflict
                detail="Пользователь с таким именем и почтой уже зарегистрирован"
            )
        

async def check_user_exists(
    email: EmailStr, 
    password: str,
    session: AsyncSession,
    redis_client: Redis,
) -> UserLogin:
    user = await get_user_by_email_from_redis(
        email=email,
        redis_client=redis_client,
    )
    if user is None:
        query = select(User.username, User.email, User.password).where(User.email == email)
        user_info = await session.execute(query)
        user = user_info.first()

        if user is None:
            raise HTTPException(status_code=404, detail="Invalid password or email")

        user_dict = {"username": user[0], "email": user[1], "password": user[2].decode("utf-8")}
        # user = {"username": user[0], "email": user[1]}

        cache_key = f"user{email}"
        # передать строку в user_dict
        await redis_client.set(cache_key, json.dumps(user_dict), ex=85400)

    # передать байты в user_dict["password"]
        if validate_password(password, user_dict["password"].encode()):
            return UserLogin.model_validate(user_dict)
    
    if validate_password(password, user["password"].encode()):
        return UserLogin.model_validate(user)

    raise HTTPException(status_code=401, detail="Invalid password")

async def get_user_by_email_from_redis(
    email: EmailStr,
    redis_client: Redis,
):
    cache_key = f"user{email}"
    if await redis_client.exists(cache_key):
        user = await redis_client.get(cache_key)
        return json.loads(user.decode("utf-8"))
    return None


async def select_user_by_email(
    email: EmailStr,
    session: AsyncSession,
) -> UserInfo:
    query = select(User.username, User.email).where(User.email == email)
    info = await session.execute(query)
    user = info.first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
        
    user_dict = {"username": user[0], "email": user[1]}
    return UserInfo.model_validate(user_dict)

async def select_user_id_by_email(
        email: EmailStr,
        session: AsyncSession,
        redis_client: Redis,
):
    cache_key = f"id{email}"
    try:
        cached_user_id = await redis_client.get(cache_key)
        if cached_user_id:
            return cached_user_id
    except:
        query = select(User.id).where(User.email == email)
        id = await session.execute(query)
        user_id = id.first()
        if user_id is None:
            raise HTTPException(status_code=404, detail="User not found")
        redis_client.set(cache_key, user_id, ex=85400)
        return user_id[0]
        

async def refresh_tokens(
    request: Request,
    redis_client: Redis = Depends(get_redis),
):
    token = request.cookies.get('refresh_token')
    user_email = await get_email_from_token(token=token, redis_client=redis_client)
    access_token = await create_access_token(user_email=user_email)
    refresh_token = await create_refresh_token(user_email=user_email)
    token = Token(
        access_token=access_token,
        refresh_token=refresh_token,
    )
    cache_refresh_token_key = f"email:{refresh_token}"
    await redis_client.set(cache_refresh_token_key, user_email, ex=85400)
    return token

async def delete_account(
    request: Request,
    password: UserPasswd,
    session: AsyncSession,
    response: Response,
    redis_client: Redis,
):
    access_token = request.cookies.get('access_token')
    user_email = await get_email_from_token(
        token=access_token,
        redis_client=redis_client,
    )
    user = await check_user_exists(
        email=user_email, 
        password=password.password,
        session=session,
        redis_client=redis_client,
    )
    cache_key = f"user:{user_email}"
    if await redis_client.exists(cache_key):
        await redis_client.delete(cache_key)
        print(f"пользователь {user_email} удалён из redis")
    query = delete(User).where(User.email == user_email)
    await session.execute(query)
    await session.commit()
    return "Successful"

async def get_email_from_token(
    token: str,
    redis_client: Redis,
):
    cache_key = f"email:{token}"
    try:
        cached_user_email = await redis_client.get(cache_key)
        if cached_user_email:
            return cached_user_email.decode("utf-8")
        
        payload = decode_jwt(token=token)
        user_email = payload.get("sub")
        if not user_email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Unauthorized"
            )
        await redis_client.set(cache_key, user_email, ex=payload.get("exp"))
        return user_email
    
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token expired"
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid token"
        )

async def get_current_auth_user(
    email: EmailStr,
    session: AsyncSession,
    redis_client: Redis,
) -> UserInfo:
    cache_key = f"user:{email}"
    cached_user_info = await redis_client.get(cache_key)

    if cached_user_info:
        return UserInfo.model_validate_json(cached_user_info)

    user_info = await select_user_by_email(email = email, session = session)
    await redis_client.set(cache_key, user_info.model_dump_json(), ex=85400)
    return user_info

async def get_user_id_from_token(
    request: Request,
    session: AsyncSession,
    redis_client: Redis,
)-> int:
    token = request.cookies.get("access_token")
    user_email = await get_email_from_token(token, redis_client=redis_client)
    user_id = await select_user_id_by_email(email = user_email, session = session, redis_client=redis_client)
    return user_id

async def create_tokens(
    user: UserLogin,
    session: AsyncSession,
    redis_client: Redis,
)-> Token:
    user = await check_user_exists(email=user.email, password=user.password, session=session, redis_client=redis_client)
    access_token = await create_access_token(user_email=user.email)
    refresh_token = await create_refresh_token(user_email=user.email)
    token = Token(
        access_token=access_token,
        refresh_token=refresh_token,
    )
    return token
