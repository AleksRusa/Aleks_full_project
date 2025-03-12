from datetime import timedelta, datetime, timezone

import bcrypt
import jwt
from fastapi import Response
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr

from config.config import settings
from schemas.user import Token, UserLogin


TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str =settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = int(datetime.now(timezone.utc).timestamp())
    if expire_timedelta:
        expire = now + int(expire_timedelta.total_seconds())
    else:
        expire = now + int(timedelta(minutes=expire_minutes).total_seconds())
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        to_encode, 
        private_key, 
        algorithm=algorithm
    )
    return encoded

def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithms: list[str] = [settings.auth_jwt.algorithm],
):
    decoded = jwt.decode(
        token.encode("utf-8"),
        public_key,
        algorithms=algorithms,
    )
    return decoded
    
def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    password_bytes = password.encode('utf-8')
    return bcrypt.hashpw(password_bytes, salt)

def validate_password(
        password: str,
        hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password
    )

def create_token_response(token: Token, response: Response):
    response.set_cookie(
        key="access_token",  # Сначала ключ
        value=token.access_token,  # Затем значение
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=int(timedelta(minutes=settings.auth_jwt.access_token_expire_minutes).total_seconds()),
        path="/",
        domain="localhost",
    )
    response.set_cookie(
        key="refresh_token",
        value=token.refresh_token,
        httponly=True,
        secure=False,
        samesite="Strict",
        max_age=2592000,
        path="/user/refresh/"  # 30 дней в секундах
    )
    return JSONResponse(content={"detail": "Login successful"}, status_code=200, headers=response.headers)

async def create_jwt(
    token_type: str,
    token_payload: dict,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None
):
    jwt_payloaad = {TOKEN_TYPE_FIELD: token_type}
    jwt_payloaad.update(token_payload)
    return encode_jwt(
        payload=jwt_payloaad,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )

async def create_access_token(
    user_email: EmailStr,
)-> str:
    jwt_payload = {
        "sub": user_email,
        "email": user_email,
    }
    return await create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_payload=jwt_payload,
        expire_minutes=settings.auth_jwt.access_token_expire_minutes,
    )

def create_refresh_token(
    user_email: EmailStr,
)-> str:
    jwt_payload = {
        "sub": user_email,
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_payload=jwt_payload,
        expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days)
    )