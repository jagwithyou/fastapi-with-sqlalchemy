from fastapi import FastAPI
from .database import engine
from . import models
from .routers import todos

models.Base.metadata.create_all(bind=engine)

app = FastAPI( title="Todo APP",
    description="This is a test todo app for the FastAPI.",
    version="1.0")

app.include_router(todos.router, prefix="/todos", tags=["todos"])
