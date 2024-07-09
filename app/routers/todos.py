from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import schemas, todo_views
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Todo)
async def create_todo(todo: schemas.TodoCreate, db: AsyncSession = Depends(get_db)):
    return await todo_views.create_todo(db=db, todo=todo)

@router.get("/", response_model=List[schemas.Todo])
async def read_todos(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await todo_views.get_todos(db=db, skip=skip, limit=limit)

@router.get("/{todo_id}", response_model=schemas.Todo)
async def read_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    db_todo = await todo_views.get_todo(db=db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.put("/{todo_id}", response_model=schemas.Todo)
async def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: AsyncSession = Depends(get_db)):
    db_todo = await todo_views.update_todo(db=db, todo_id=todo_id, todo=todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.delete("/{todo_id}", response_model=schemas.Todo)
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    db_todo = await todo_views.delete_todo(db=db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo
