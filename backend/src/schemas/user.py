from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    first_name: str = Field(max_length=16)
    last_name: str = Field(max_length=16)
    age: int = Field(gt=0, le=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=255)

class TodoCreate(BaseModel):
    description: str

class TodoResponse(TodoCreate):
    id: int
    is_done: bool
    user_id: int