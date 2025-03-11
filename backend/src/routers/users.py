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

from database.database import get_db
from schemas.user import UserCreate, UserLogin, Token, UserInfo, UserSchema, UserDelete
from crud.user import create_user, get_current_auth_user, check_user_exists, create_new_tokens, delete_account
from auth.utils import (
    hash_password, 
    encode_jwt, 
    decode_jwt, 
    create_token_response, 
    create_access_token,
    create_refresh_token,
)

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register/")
async def register_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_db),
):
    user = UserSchema(
        username=user_data.username,
        email=user_data.email,
        password=hash_password(user_data.password)
    )
    return await create_user(session, user)

@router.delete("/delete_user/")
async def delete_user(
    user_passwd: UserDelete,
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_db),
):
    deleted = await delete_account(
        request=request,
        password=user_passwd,
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
) -> Response:
    user = await check_user_exists(email=user.email, password=user.password, session=session)
    access_token = await create_access_token(user_email=user.email)
    refresh_token = await create_refresh_token(user_email=user.email)
    token = Token(
        access_token=access_token,
        refresh_token=refresh_token,
    )
    return create_token_response(token=token, response=response)

@router.get("/me/", response_model=UserInfo)
async def get_user_info(
    user: UserInfo = Depends(get_current_auth_user),
) -> UserInfo:
    return user

@router.get("/refresh/")
async def refresh_tokens(
    response: Response,
    token: Token = Depends(create_new_tokens),
):
    return create_token_response(token=token, response=response)
