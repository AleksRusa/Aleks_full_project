from uuid import UUID
from pydantic import BaseModel

class TodoTask(BaseModel):
    uuid: UUID
    description: str

class TodotaskInfo(BaseModel):
    uuid: UUID
    description: str
    is_done: bool


class TodoTaskStatus(BaseModel):
    uuid: UUID
    is_done: bool
