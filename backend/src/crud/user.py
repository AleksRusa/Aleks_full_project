from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, values
from fastapi import Form

from schemas.user import UserCreate
from auth.utils import hash_password
from database.models import User

async def create_user(session: AsyncSession, user_data: UserCreate):
    user_dict = user_data.model_dump(exclude_unset=True)
    user = User(**user_dict)
    session.add(user)
    await session.commit()
    session.refresh(user)
    return f"пользователь {user.first_name} успешно зарегистрирован"
