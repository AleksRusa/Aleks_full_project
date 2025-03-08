from uuid import UUID
from pydantic import BaseModel

class TodoTask(BaseModel):
    uuid: UUID
    description: str

class TodotaskResponse(BaseModel):
    uuid: UUID
    description: str
    user_id: int


class TodoTaskStatus(BaseModel):
    uuid: UUID
    is_done: bool
