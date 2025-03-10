from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update
from fastapi import Request, Depends

from database.database import get_db
from database.models import Todolist
from schemas.todotask import TodoTask, TodotaskInfo, TodoTaskStatus
from crud.user import get_user_id_from_token

async def create_task(session: AsyncSession, todotask: TodoTask, user_id: int):
    task = await session.execute(
        insert(Todolist).values(
            uuid=todotask.uuid,
            description=todotask.description,
            user_id=user_id,
            is_done=False
        ).returning(Todolist)
    )
    await session.commit()
    return {"message": "Created successfully"}

async def select_user_tasks(
    session: AsyncSession,
    request: Request,
)-> list[TodotaskInfo]:
    id_from_token = await get_user_id_from_token(session=session, request=request)
    query = select(Todolist).where(Todolist.user_id == id_from_token)
    NotesInfo = await session.execute(query)
    Notes = NotesInfo.scalars().all()

    if not Notes:
        return []
    
    print(Notes)
    UserNotes = [
        TodotaskInfo(
            uuid=note.uuid, 
            description=note.description, 
            is_done=note.is_done,
        )
        for note in Notes]
    print(UserNotes)
    return UserNotes

async def change_task_status(
    session: AsyncSession,
    task: TodoTaskStatus,
)-> dict:
    query = update(Todolist).where(Todolist.uuid == task.uuid).values(is_done=task.is_done)
    await session.execute(query)
    await session.commit()
    if task.is_done == True:
        return {"message": "task is done"}
    else:
        return {"message": "you need to do it"}

async def change_task_body(
    session: AsyncSession,
    task: TodoTask,
)-> dict:
    query = update(Todolist).where(Todolist.uuid == task.uuid).values(description=task.description)
    await session.execute(query)
    await session.commit()
    return {"message": "you changed your task"}