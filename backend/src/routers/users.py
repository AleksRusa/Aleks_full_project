from fastapi import (
    APIRouter,
    HTTPException,
    Form,
    Depends,
    status,
    Query
)
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from schemas.user import UserCreate, UserLogin, Token
from crud.user import create_user, select_user_info, validate_user_login
from auth.utils import hash_password, encode_jwt

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/register/")
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

@router.get("/info/")
async def get_user_info(
    user_id: int = Query(..., description="User ID"),
    session: AsyncSession = Depends(get_db)
):
    return await select_user_info(session, user_id)

@router.post("/login/", response_model=Token)
def auth_user_issue_jwt(
    user: UserLogin = Depends(validate_user_login),
    # session: AsyncSession = Depends(get_db)
):
    jwt_payload = {
        "sub": user.id,
        "email": user.email,
        # "exp":  
    }
    token = encode_jwt()
    return Token(
        access_token=token,
        token_type="Bearer",
    )