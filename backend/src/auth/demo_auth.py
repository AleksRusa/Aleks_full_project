from fastapi import (
    APIRouter
)

from schemas.user import UserSchema
from auth import utils as auth_utils

# auth_router = 