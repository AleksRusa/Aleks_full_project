from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from fastapi import Request

from database.models import Todolist
from schemas.todotask import TodoTask
from crud.user import get_user_id_from_token

async def create_task(session: AsyncSession, todolist: TodoTask):
    task = await session.execute(
        insert(Todolist).values(
            description=todolist.description,
            user_id=todolist.user_id,
            is_done=False
        ).returning(Todolist)
    )
    task_obj = task.scalar()
    task_dict = {column.name: getattr(task_obj, column.name) for column in Todolist.__table__.columns}
    await session.commit()
    return TodoTask.model_validate(task_dict)

async def select_user_tasks(
    session: AsyncSession, 
    request: Request,
):
    user = get_user_id_from_token(request=request)
