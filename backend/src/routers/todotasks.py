from fastapi import APIRouter, Depends, HTTPException, Request, Query
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from schemas.todotask import TodoTask, TodoTaskResponse
from crud.todotask import create_task, select_user_tasks

router = APIRouter(prefix="/todolist", tags=["todolist"])

templates = Jinja2Templates(directory="src/templates")

@router.post("/", response_model=TodoTaskResponse)
async def create_todotask(
    todotask: TodoTask,
    session: AsyncSession = Depends(get_db)
):
    return await create_task(session, todotask)

@router.get("/write_task")
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/get_user_tasks/", response_model=list[TodoTaskResponse])
async def user_tasks(
        user_id: int = Query(..., description="ID пользователя"),  # Параметр запроса
    db: AsyncSession = Depends(get_db)
):
    return await select_user_tasks(db, user_id)