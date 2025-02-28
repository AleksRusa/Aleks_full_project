from datetime import timedelta, datetime, timezone

import bcrypt
import jwt

from database.config import settings


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
        token,
        public_key,
        algorithms=algorithms,
    )
    return decoded
    
def hash_password(
        password: str,
) -> str:
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