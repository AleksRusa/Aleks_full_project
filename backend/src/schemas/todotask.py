from pydantic import BaseModel

class TodoTask(BaseModel):
    description: str
    user_id: int


class TodoTaskResponse(TodoTask):
    id: int
    is_done: bool
