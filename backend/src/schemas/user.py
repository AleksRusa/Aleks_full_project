from pydantic import BaseModel, Field, ConfigDict, EmailStr

class UserInfo(BaseModel):
    first_name: str = Field(max_length=64)
    last_name: str = Field(max_length=64)
    age: int = Field(gt=0, le=100)
    email: EmailStr
class UserCreate(UserInfo):
    password: bytes = Field(min_length=8, max_length=128)

class UserSchema(UserInfo):
    model_config = ConfigDict(string=True)
    
    password: bytes = Field(min_length=8, max_length=128)

class UserLogin(BaseModel):
    first_name: str
    email: EmailStr
    password: bytes = Field(min_length=8, max_length=128)

class Token(BaseModel):
    access_token: str
    token_type: str 