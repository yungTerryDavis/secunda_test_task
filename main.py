from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Path, Query

from database import async_session_maker
from dependencies import area_query, get_service
from init_database import is_db_data_present, populate_db
from schemas import (
    BoxArea,
    BuildingSchema,
    CircleArea,
    OrganizationFullSchema,
    OrganizationSchema,
    PracticeSchema,
)
from service import SecundaService


@asynccontextmanager
async def lifespan(app: FastAPI):  # pyright:ignore[reportUnusedParameter]
    async with async_session_maker() as session:
        if not await is_db_data_present(session):
            print("No data found. Populating DB...")
            await populate_db(session)
    yield


app = FastAPI(lifespan=lifespan)

# ----------- SUPPORTING FUNCTIONALITY -----------

@app.get("/buildings/all")
async def list_all_buildings(
    service: Annotated[SecundaService, Depends(get_service)],
) -> list[BuildingSchema]:
    return await service.list_all_buildings()


@app.get("/practices/all")
async def list_all_practices(
    service: Annotated[SecundaService, Depends(get_service)],
) -> list[PracticeSchema]:
    return await service.list_all_practices()


@app.get("/organizations/all")
async def list_all_organizations(
    service: Annotated[SecundaService, Depends(get_service)],
) -> list[OrganizationSchema]:
    return await service.list_all_organizations()

# ----------- MAIN FUNCTIONALITY -----------

@app.get("/building/{building_id}/organizations")
async def list_organizations_in_building(
    building_id: Annotated[int, Path(gt=0)],
    service: Annotated[SecundaService, Depends(get_service)],
) -> list[OrganizationSchema]:
    return await service.list_organizations_in_building(building_id)


@app.get("/practice/{practice_id}/organizations")
async def list_organizations_of_practice(
    practice_id: Annotated[int, Path(gt=0)],
    service: Annotated[SecundaService, Depends(get_service)],
) -> list[OrganizationSchema]:
    return await service.list_organizations_of_practice(practice_id)


@app.get("/buildings/search_in_area")
async def list_buildings_in_area(
    area: Annotated[BoxArea | CircleArea, Depends(area_query)],
    service: Annotated[SecundaService, Depends(get_service)],
) -> list[BuildingSchema]:
    return await service.list_buildings_in_area(area)


@app.get("/organizations/search_in_area")
async def list_organizations_in_area(
    area: Annotated[BoxArea | CircleArea, Depends(area_query)],
    service: Annotated[SecundaService, Depends(get_service)],
) -> list[OrganizationSchema]:
    return await service.list_organizations_in_area(area)


@app.get("/organization/{organization_id}")
async def get_organization(
    organization_id: Annotated[int, Path(gt=0)],
    service: Annotated[SecundaService, Depends(get_service)],
) -> OrganizationFullSchema:
    return await service.get_organization(organization_id)


@app.get("/practice/{practice_id}/organizations/recursive")
async def list_organizations_of_practice_recursively(
    practice_id: Annotated[int, Path(gt=0)],
    service: Annotated[SecundaService, Depends(get_service)],
) -> list[OrganizationSchema]:
    return await service.list_organizations_of_practice_recursively(practice_id)


@app.get("/organizations/search_by_name")
async def list_organizations_by_name_search(
    search: Annotated[str, Query(min_length=1)],
    service: Annotated[SecundaService, Depends(get_service)],
) -> list[OrganizationSchema]:
    return await service.search_organizations_by_name(search)
