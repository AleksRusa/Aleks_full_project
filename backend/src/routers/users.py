from fastapi import (
    APIRouter,
    HTTPException,
    Form,
    Depends,
    status,
    Query
)
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from database.database import get_db
from schemas.user import UserCreate, UserLogin, Token, UserInfo
from crud.user import create_user, get_current_auth_user, check_user_exists
from auth.utils import hash_password, encode_jwt, decode_jwt

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register/")
async def register_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_db),
):
    user = UserCreate(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        age=user_data.age,
        email=user_data.email,
        password=hash_password(user_data.password)
    )
    return await create_user(session, user)


@router.post("/login/")
async def auth_user_issue_jwt(
    user: UserLogin,
    session: AsyncSession = Depends(get_db),
):
    user = await check_user_exists(email=user.email, password=user.password, session=session)
    jwt_payload = {
        "sub": user.email,
        "email": user.email,
    }
    token = encode_jwt(jwt_payload)
    token = Token(
        access_token=token,
        token_type="Bearer",
    )
    return token


@router.get("/info/", response_model=UserInfo)
async def get_user_info(
    user: UserInfo = Depends(get_current_auth_user)
) -> UserInfo:
    return user

