from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from schemas.todotask import TodoTask, TodoTaskStatus, TodotaskResponse
from crud.todotask import create_task, select_user_tasks
from crud.user import get_user_id_from_token

router = APIRouter(prefix="/todolist", tags=["todolist"])


@router.post("/createTask/", response_model=TodoTask)
async def create_todotask(
    request: Request,
    todotask: TodoTask,
    session: AsyncSession = Depends(get_db)
):
    id = get_user_id_from_token(request=request)
    return await create_task(session=session, todotask=todotask, user_id=id)


@router.get("/get_user_tasks/", response_model=list[TodoTask])
async def user_tasks(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    return await select_user_tasks(db)

@router.post("/taskDone/")
async def change_task_status():
    pass


@router.post("/updateTask/")
async def update_task_body():
    pass
