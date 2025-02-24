from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from database.models import Users

from database.models import Todolist
from schemas.todotask import TodoTask, TodoTaskResponse

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
    return TodoTaskResponse.model_validate(task_dict)

async def select_user_tasks(session: AsyncSession, user_id: int):
    result = await session.execute(
        select(Todolist).where(Todolist.user_id == user_id)
    )
    return result.scalars().all()
