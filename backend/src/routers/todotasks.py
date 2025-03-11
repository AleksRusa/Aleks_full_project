from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from schemas.todotask import TodoTask, TodoTaskStatus, TodotaskInfo, TaskId
from crud.todotask import create_task, select_user_tasks, change_task_status, change_task_body, delete_task_by_id
from crud.user import get_user_id_from_token

router = APIRouter(prefix="/todolist", tags=["todolist"])


@router.post("/createTask/")
async def create_todotask(
    request: Request,
    todotask: TodoTask,
    session: AsyncSession = Depends(get_db)
):
    id = await get_user_id_from_token(request=request, session=session)
    return await create_task(session=session, todotask=todotask, user_id=id)


@router.get("/get_user_tasks/", response_model=list[TodotaskInfo])
async def user_tasks(
    request: Request,
    session: AsyncSession = Depends(get_db),
):
    return await select_user_tasks(session=session, request=request)

@router.patch("/taskDone/")
async def task_status(
    task: TodoTaskStatus,
    session: AsyncSession = Depends(get_db),
):
    return await change_task_status(session=session, task=task)

@router.patch("/updateTask/")
async def update_task_body(
    task: TodoTask,
    session: AsyncSession = Depends(get_db)
):
    return await change_task_body(session=session, task=task)

@router.delete("/deleteTask/")
async def delete_task(
    task_id: TaskId,
    session: AsyncSession = Depends(get_db),
):
    return await delete_task_by_id(task_id=task_id.uuid, session=session)