from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Path, Query

from database import async_session_maker
from dependencies import area_query, get_service, verify_api_key
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

# ----------- SUPPORTING FUNCTIONALITY -----------

@app.get(
    "/buildings/all",
    description="Вывод списка всех зданий.",
    tags=["buildings"],
)
async def list_all_buildings(
    service: Annotated[SecundaService, Depends(get_service)],
    _: Annotated[str, Depends(verify_api_key)],
) -> list[BuildingSchema]:
    return await service.list_all_buildings()


@app.get(
    "/practices/all",
    description="Вывод списка всех деятельностей.",
    tags=["practices"],
)
async def list_all_practices(
    service: Annotated[SecundaService, Depends(get_service)],
    _: Annotated[str, Depends(verify_api_key)],
) -> list[PracticeSchema]:
    return await service.list_all_practices()


@app.get(
    "/organizations/all",
    description="Вывод списка всех организаций.",
    tags=["organizations"],
)
async def list_all_organizations(
    service: Annotated[SecundaService, Depends(get_service)],
    _: Annotated[str, Depends(verify_api_key)],
) -> list[OrganizationSchema]:
    return await service.list_all_organizations()

# ----------- MAIN FUNCTIONALITY -----------

@app.get(
    "/building/{building_id}/organizations",
    description="Вывод списка всех организаций внутри данного здания.",
    tags=["organizations"],
)
async def list_organizations_in_building(
    building_id: Annotated[int, Path(gt=0, description="Id Здания")],
    service: Annotated[SecundaService, Depends(get_service)],
    _: Annotated[str, Depends(verify_api_key)],
) -> list[OrganizationSchema]:
    return await service.list_organizations_in_building(building_id)


@app.get(
    "/practice/{practice_id}/organizations",
    description="Вывод списка всех организаций, занятых данным видом деятельности.",
    tags=["organizations"],
)
async def list_organizations_of_practice(
    practice_id: Annotated[int, Path(gt=0, description="Id деятельности")],
    service: Annotated[SecundaService, Depends(get_service)],
    _: Annotated[str, Depends(verify_api_key)],
) -> list[OrganizationSchema]:
    return await service.list_organizations_of_practice(practice_id)


@app.get(
    "/buildings/search_in_area",
    description=(
        "Вывод списка всех зданий в заданной области. Область можно задать "
        "одним из 2 способов:\n1. С помощью 2-х точек, образующих прямоугольную "
        "область;\n2. С помощью центральной точки и радиуса, образующих круглую область."
    ),
    tags=["buildings"],
)
async def list_buildings_in_area(
    area: Annotated[BoxArea | CircleArea, Depends(area_query)],
    service: Annotated[SecundaService, Depends(get_service)],
    _: Annotated[str, Depends(verify_api_key)],
) -> list[BuildingSchema]:
    return await service.list_buildings_in_area(area)


@app.get(
    "/organizations/search_in_area",
    description=(
        "Вывод списка всех организаций в заданной области. Область можно задать "
        "одним из 2 способов:\n1. С помощью 2-х точек, образующих прямоугольную "
        "область;\n2. С помощью центральной точки и радиуса, образующих круглую область."
    ),
    tags=["organizations"],
)
async def list_organizations_in_area(
    area: Annotated[BoxArea | CircleArea, Depends(area_query)],
    service: Annotated[SecundaService, Depends(get_service)],
    _: Annotated[str, Depends(verify_api_key)],
) -> list[OrganizationSchema]:
    return await service.list_organizations_in_area(area)


@app.get(
    "/organization/{organization_id}",
    description="Вывод подробной информации о данной организации.",   
    tags=["organizations"],
)
async def get_organization(
    organization_id: Annotated[int, Path(gt=0, description="Id организации")],
    service: Annotated[SecundaService, Depends(get_service)],
    _: Annotated[str, Depends(verify_api_key)],
) -> OrganizationFullSchema:
    return await service.get_organization(organization_id)


@app.get(
    "/practice/{practice_id}/organizations/recursive",
    description=
    (
        "Вывод списка организаций, занятых данной деятельностью или "
        "деятельностью, являющейся одним из потомков данной деятельности."
    ),
    tags=["organizations"],
)
async def list_organizations_of_practice_recursively(
    practice_id: Annotated[int, Path(gt=0, description="Id деятельности")],
    service: Annotated[SecundaService, Depends(get_service)],
    _: Annotated[str, Depends(verify_api_key)],
) -> list[OrganizationSchema]:
    return await service.list_organizations_of_practice_recursively(practice_id)


@app.get(
    "/organizations/search_by_name",
    description="Вывод списка организаций, с названием, включающим данную подстроку.",
    tags=["organizations"],
)
async def list_organizations_by_name_search(
    search: Annotated[str, Query(min_length=1, description="Искомая подстрока")],
    service: Annotated[SecundaService, Depends(get_service)],
    _: Annotated[str, Depends(verify_api_key)],
) -> list[OrganizationSchema]:
    return await service.search_organizations_by_name(search)
