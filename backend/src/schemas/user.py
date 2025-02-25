from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserCreate(BaseModel):
    first_name: str = Field(max_length=16)
    last_name: str = Field(max_length=16)
    age: int = Field(gt=0, le=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=255)

class UserSchema(BaseModel):
    model_config = ConfigDict(string=True)

    first_name: str
    last_name: str
    age: int
    email: EmailStr
    password: bytes
