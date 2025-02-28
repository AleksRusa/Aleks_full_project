from jwt import InvalidTokenError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, values, select
from fastapi import Form, HTTPException, Depends, status
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
    except ValidationError as e:
        # Обработка ошибок валидации Pydantic
        raise HTTPException(
            status_code=422,  # Unprocessable Entity
            detail=f"Ошибка валидации данных: {e}"
        )
    except IntegrityError as e:
        # Обработка конфликта уникальности (например, дублирующийся email)
        if "users_email_key" in str(e.orig):
            raise HTTPException(
                status_code=409,  # Conflict
                detail="Email уже существует"
            )
        else:
            raise HTTPException(
                status_code=400,  # Bad Request
                detail="Неизвестная ошибка базы данных"
            )

async def validate_user_login(
    user_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db),
):
    user_login = await check_user_exists(user_data.username, user_data.password, session)
    return user_login

async def check_user_exists(
    email: EmailStr, 
    password: str,
    session: AsyncSession,
) -> UserLogin:
    query = select(User.first_name, User.email, User.password).where(User.email == email)
    user_info = await session.execute(query)
    user = user_info.first()
    
    #checking if user exists
    if user is None:
        raise HTTPException(status_code=404, detail="Invalid password or email")

    user_dict = {"first_name": user[0], "email": user[1], "password": user[2]}

    # cheking is password correct
    if validate_password(password, user_dict["password"]):
        return UserLogin.model_validate(user_dict)

    raise HTTPException(status_code=401, detail="Invalid password")

async def select_user_info(
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
        # credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_db)
) -> UserInfo:
    print(token)
    # token = credentials.credentials
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

    user_email = payload.get("email")
    if not user_email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    user_info = await select_user_info(email = user_email, session = session)
    return user_info