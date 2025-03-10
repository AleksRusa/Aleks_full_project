from jwt import InvalidTokenError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, values, select
from fastapi import HTTPException, Depends, status, Request
from fastapi.security import (
    HTTPBearer, 
    HTTPAuthorizationCredentials, 
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from pydantic import ValidationError, EmailStr

from schemas.user import UserCreate, UserInfo, UserLogin
from auth.utils import hash_password, validate_password, decode_jwt
from database.models import User
from database.database import get_db

# http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login/")

async def create_user(session: AsyncSession, user_data: UserCreate):
    try:
        user_dict = user_data.model_dump(exclude_unset=True)
        user = User(**user_dict)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return f"пользователь {user.first_name} успешно зарегистрирован"
    except IntegrityError as e:
        # Обработка конфликта уникальности (например, дублирующийся email)
        if "users_email_key" in str(e.orig):
            raise HTTPException(
                status_code=409,  # Conflict
                detail="Пользователь с таким email уже зарегистрирован"
            )
        

async def check_user_exists(
    email: EmailStr, 
    password: str,
    session: AsyncSession,
) -> UserLogin:
    query = select(User.email, User.password).where(User.email == email)
    user_info = await session.execute(query)
    user = user_info.first()
    
    if user is None:
        raise HTTPException(status_code=404, detail="Invalid password or email")

    user_dict = {"email": user[0], "password": user[1]}

    if validate_password(password, user_dict["password"]):
        return UserLogin.model_validate(user_dict)

    raise HTTPException(status_code=401, detail="Invalid password")


async def select_user_by_email(
        email: str,
        session: AsyncSession,
) -> UserInfo:
    query = select(User.first_name, User.last_name, User.age, User.email).where(User.email == email)
    info = await session.execute(query)
    user = info.first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_dict = {"first_name": user[0], "last_name": user[1], "age": user[2], "email": user[3]}
    return UserInfo.model_validate(user_dict)


async def get_current_auth_user(
    request: Request,
    session: AsyncSession = Depends(get_db),
) -> UserInfo:
    token = request.cookies.get('access_token')  # Получаем токен из куки
    token = token.replace("Bearer ", "")
    if token is None:
        raise HTTPException(status_code=401, detail="Токен отсутствует")
    try:
        payload = decode_jwt(
            token=token,
        )  
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
    user_email = payload.get("sub")
    if not user_email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    user_info = await select_user_by_email(email = user_email, session = session)
    return user_info