from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import async_session_maker
from init_database import is_db_data_present, populate_db


@asynccontextmanager
async def lifespan(app: FastAPI):  # pyright:ignore[reportUnusedParameter]
    async with async_session_maker() as session:
        if not await is_db_data_present(session):
            print("No data found. Populating DB...")
            await populate_db(session)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"msg": "Hello World!"}
