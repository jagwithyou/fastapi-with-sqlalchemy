from fastapi import FastAPI
from .database import engine, Base, database
from .routers import todos

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(todos.router, prefix="/todos", tags=["todos"])
