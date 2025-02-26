from pydantic import BaseModel, Field, ConfigDict

class UserCreate(BaseModel):
    first_name: str = Field(max_length=16)
    last_name: str = Field(max_length=16)
    age: int = Field(gt=0, le=100)
    email: str = Field(max_length=100)
    password: bytes = Field(min_length=8, max_length=128)

class UserSchema(BaseModel):
    model_config = ConfigDict(string=True)

    first_name: str
    last_name: str
    age: int
    email: str
    password: bytes
