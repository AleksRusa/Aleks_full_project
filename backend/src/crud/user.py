import asyncio

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

from schemas.user import UserInfo, UserLogin, UserSchema, Token, UserDelete
from auth.utils import (
    validate_password, 
    decode_jwt,
    create_access_token,
    create_refresh_token,
)
from database.models import User
from database.database import get_db
from redis_client import get_redis

async def create_user(session: AsyncSession, user_data: UserSchema):
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
) -> UserLogin:
    query = select(User.username, User.email, User.password).where(User.email == email)
    user_info = await session.execute(query)
    user = user_info.first()
    
    if user is None:
        raise HTTPException(status_code=404, detail="Invalid password or email")

    user_dict = {"username": user[0], "email": user[1], "password": user[2]}

    if validate_password(password, user_dict["password"]):
        return UserLogin.model_validate(user_dict)

    raise HTTPException(status_code=401, detail="Invalid password")


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
):
    query = select(User.id).where(User.email == email)
    id = await session.execute(query)
    user_id = id.first()
    if user_id is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_id[0]
        

async def refresh_tokens(
    request: Request,
):
    refresh_token = request.cookies.get('refresh_token')
    user_email = await get_email_from_token(refresh_token)
    access_token = await create_access_token(user_email=user_email)
    refresh_token = await create_refresh_token(user_email=user_email)
    token = Token(
        access_token=access_token,
        refresh_token=refresh_token,
    )
    return token

async def delete_account(
    request: Request,
    password: UserDelete,
    session: AsyncSession,
    response: Response
):
    user_email = await get_user_email_from_token(request=request)
    user = check_user_exists(
        email=user_email, 
        password=password,
        session=session,
    )
    query = delete(User).where(User.email == user_email)
    await session.execute(query)
    await session.commit()
    return "Successful"
    
    

async def get_user_email_from_token(
    request: Request,                  
):
    access_token = request.cookies.get('access_token')
    
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
    email = await get_email_from_token(access_token)
    return email

async def get_email_from_token(
    token: str,
    redis_client: Redis
):
    cache_key = f"email:{token}"
    try:
        cached_user_email = await redis_client.get(cache_key)
        if cached_user_email:
            print("was cached")
            return cached_user_email.decode("utf-8")
        
        payload = decode_jwt(token=token)
        user_email = payload.get("sub")
        if not user_email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Unauthorized"
            )
        print("added to cache")
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
    user_email: EmailStr,
    session: AsyncSession,
    redis_client: Redis,
) -> UserInfo:
    cache_key = f"user:{user_email}"
    cached_user_info = await redis_client.get(cache_key)

    if cached_user_info:
        return UserInfo.model_validate_json(cached_user_info)

    user_info = await select_user_by_email(email = user_email, session = session)
    await redis_client.set(cache_key, user_info.model_dump_json(), ex=86400)
    return user_info

async def get_user_id_from_token(
    request: Request,
    session: AsyncSession,
)-> int:
    user_email = await get_user_email_from_token(request=request)

    user_id = await select_user_id_by_email(email = user_email, session = session)
    return user_id

async def create_tokens(
    user: UserLogin,
    session: AsyncSession,
)-> Token:
    user = await check_user_exists(email=user.email, password=user.password, session=session)
    access_token = await create_access_token(user_email=user.email)
    refresh_token = await create_refresh_token(user_email=user.email)
    token = Token(
        access_token=access_token,
        refresh_token=refresh_token,
    )
    return token
