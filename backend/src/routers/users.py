from fastapi import (
    APIRouter,
    HTTPException,
    Form,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from schemas.user import UserCreate
from crud.user import create_user
from auth.utils import hash_password

user_router = APIRouter(prefix="/auth", tags=["auth"])

@user_router.post("/register/")
async def register_user(
    first_name: str = Form(min_length=2, max_length=50),
    last_name: str = Form(min_length=2, max_length=50),
    age: int = Form(ge=0, le=100),
    email: str = Form(max_length=100),
    password: str = Form(min_length=6, max_length=128),
    session: AsyncSession = Depends(get_db),
):
    user = UserCreate(
        first_name=first_name,
        last_name=last_name,
        age=age,
        email=email,
        password=hash_password(password)
    )
    return await create_user(session, user)