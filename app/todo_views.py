from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .exceptions import async_exception_handler_decorator
from . import models, schemas

@async_exception_handler_decorator
async def get_todo(db: AsyncSession, todo_id: int):
    result = await db.execute(select(models.Todo).filter(models.Todo.id == todo_id))
    return result.scalars().first()

@async_exception_handler_decorator
async def get_todos(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.Todo).offset(skip).limit(limit))
    return result.scalars().all()

@async_exception_handler_decorator
async def create_todo(db: AsyncSession, todo: schemas.TodoCreate):
    db_todo = models.Todo(**todo.dict())
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo

@async_exception_handler_decorator
async def update_todo(db: AsyncSession, todo_id: int, todo: schemas.TodoUpdate):
    db_todo = await get_todo(db, todo_id)
    if db_todo:
        for key, value in todo.dict().items():
            setattr(db_todo, key, value)
        await db.commit()
        await db.refresh(db_todo)
    return db_todo

@async_exception_handler_decorator
async def delete_todo(db: AsyncSession, todo_id: int):
    db_todo = await get_todo(db, todo_id)
    if db_todo:
        await db.delete(db_todo)
        await db.commit()
    return db_todo
