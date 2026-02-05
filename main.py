from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Path, Query

from database import async_session_maker
from dependencies import area_query, get_service, verify_api_key
from init_database import is_db_data_present, populate_db
from routes.router import router
from schemas import (
    BoxArea,
    BuildingSchema,
    CircleArea,
    OrganizationFullSchema,
    OrganizationSchema,
)
from service import SecundaService


@asynccontextmanager
async def lifespan(app: FastAPI):  # pyright:ignore[reportUnusedParameter]
    async with async_session_maker() as session:
        if not await is_db_data_present(session):
            print("No data found. Populating DB...")
            await populate_db(session)
    yield


tags_metadata = [
    {
        "name": "buildings",
        "description": "Методы для вывода информации о зданиях.",
    },
    {
        "name": "practices",
        "description": "Методы для вывода информации о деятельностях",
    },
    {
        "name": "organizations",
        "description": "Методы для вывода информации об организациях.",
    },
]

app = FastAPI(lifespan=lifespan, openapi_tags=tags_metadata)
app.include_router(router)
