from typing import Annotated

from fastapi import APIRouter, Depends, Path

from dependencies import area_query, get_service, verify_api_key
from schemas import BoxArea, BuildingSchema, CircleArea, OrganizationSchema
from service import SecundaService


router = APIRouter(prefix="/buildings")


@router.get(
    "/all",
    description="Вывод списка всех зданий.",
    tags=["buildings"],
)
async def list_all_buildings(
    service: Annotated[SecundaService, Depends(get_service)],
    _: Annotated[str, Depends(verify_api_key)],
) -> list[BuildingSchema]:
    return await service.list_all_buildings()


@router.get(
    "/{building_id}/organizations",
    description="Вывод списка всех организаций внутри данного здания.",
    tags=["organizations"],
)
async def list_organizations_in_building(
    building_id: Annotated[int, Path(gt=0, description="Id Здания")],
    service: Annotated[SecundaService, Depends(get_service)],
    _: Annotated[str, Depends(verify_api_key)],
) -> list[OrganizationSchema]:
    return await service.list_organizations_in_building(building_id)


@router.get(
    "/search_in_area",
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
