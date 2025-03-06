from datetime import timedelta, datetime, timezone

import bcrypt
import jwt
from fastapi import Response
from fastapi.responses import JSONResponse

from config.config import settings
from schemas.user import Token


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str =settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
):
    to_encode = payload.copy()
    now = int(datetime.now(timezone.utc).timestamp())
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
        token,
        public_key,
        algorithms=algorithms,
    )
    return decoded
    
def hash_password(password) -> str:
    if isinstance(password, bytes):
        password = password.decode('utf-8')
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)

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
        key="access_token",
        value=f"Bearer {token.access_token}",
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=int(timedelta(minutes=settings.auth_jwt.access_token_expire_minutes).total_seconds()),
        path="/",
        domain="localhost",
    )
    return JSONResponse(content={"detail": "Login successful"}, status_code=200, headers=response.headers)
