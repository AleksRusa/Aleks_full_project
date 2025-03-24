from datetime import timedelta

from fastapi import (
    APIRouter,
    HTTPException,
    Form,
    Depends,
    status,
    Query,
    Response,
    Request,
)
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import Response, JSONResponse
from redis.asyncio import Redis

from database.database import get_db
from schemas.user import UserCreate, UserLogin, Token, UserInfo, UserSchema, UserPasswd
from crud.user import create_user, get_current_auth_user, refresh_tokens, delete_account, create_tokens, get_email_from_token
from auth.utils import hash_password, create_token_response
from redis_client import get_redis


router = APIRouter(prefix="/user", tags=["user"])

@router.post("/register/")
async def register_user(
    user_data: UserCreate,
    response: Response,
    session: AsyncSession = Depends(get_db),
    redis_client: Redis = Depends(get_redis)
):
    user_login = UserLogin(email=user_data.email, password=user_data.password)
    user = UserSchema(
        username=user_data.username,
        email=user_data.email,
        password=hash_password(user_data.password)
    )
    await create_user(session, user)
    token = await create_tokens(user=user_login, session=session, redis_client=redis_client)
    return create_token_response(token=token, response=response)

@router.delete("/delete_user/")
async def delete_user(
    user_passwd: UserPasswd,
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_db),
    redis_client: Redis = Depends(get_redis),
):
    deleted = await delete_account(
        request=request,
        password=user_passwd,
        redis_client=redis_client,
        session=session,
        response=response,
    )
    if deleted == "Successful":
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}

@router.post("/login")
async def auth_user_issue_jwt(
    user: UserLogin,
    response: Response,
    session: AsyncSession = Depends(get_db),
    redis_client: Redis = Depends(get_redis),
) -> Response:
    token = await create_tokens(user=user, session=session, redis_client=redis_client)
    return create_token_response(token=token, response=response)

@router.get("/me/", response_model=UserInfo)
async def get_user_info(
    request: Request,
    session: AsyncSession = Depends(get_db),
    redis_client: Redis = Depends(get_redis),
) -> UserInfo:
    access_token = request.cookies.get('access_token')
    if not access_token:
        raise HTTPException(status_code=401, detail="Refresh token is missing")
    user_email = await get_email_from_token(
        token=access_token,
        redis_client=redis_client,
    )
    user = await get_current_auth_user(
        email=user_email, 
        session=session,
        redis_client=redis_client,
    )
    return user

@router.get("/refresh/")
async def refresh_access_and_refresh_tokens(
    response: Response,
    token: Token = Depends(refresh_tokens),
):
    return create_token_response(token=token, response=response)
