from pydantic import BaseModel, Field, ConfigDict, EmailStr

class UserInfo(BaseModel):
    username: str = Field(max_length=64)
    email: EmailStr
    
class UserDelete(BaseModel):
    password: str = Field(min_length=8, max_length=128)
class UserCreate(UserInfo):
    password: str = Field(min_length=8, max_length=128)

class UserSchema(UserInfo):
    password: bytes

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"