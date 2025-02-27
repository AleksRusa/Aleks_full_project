from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, values, select
from fastapi import Form, HTTPException, Depends
from pydantic import ValidationError, EmailStr

from schemas.user import UserCreate, UserInfo, UserLogin
from auth.utils import hash_password, validate_password
from database.models import User
from database.database import get_db

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
        
async def select_user_info(session: AsyncSession, id: int):
    query = select(User).where(User.id == id)
    info = await session.execute(query)

    if info is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = info.scalar_one()
    user_dict = {c.name: getattr(user, c.name) for c in user.__table__.columns}
    return UserInfo.model_validate(user_dict)

async def validate_user_login(
    email: str = Form(max_length=100),
    password: str = Form(min_length=8, max_length=128),
    session: AsyncSession = Depends(get_db),
):
    user_login = await check_user_exists(email, password, session)
    return user_login

async def check_user_exists(
    email: EmailStr, 
    password: str,
    session: AsyncSession,
):
    query = select(User.id, User.email, User.password).where(User.email == email)
    user_info = await session.execute(query)
    user = user_info.first()
    
    #checking user
    if user is None:
        raise HTTPException(status_code=404, detail="Invalid password or email")

    user_login = {"id": user[0], "email": user[1], "password": user[2]}

    # cheking password
    if not validate_password(password, user_login["password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    return UserLogin.model_validate(user_login)