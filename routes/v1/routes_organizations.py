from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from dependencies import area_query, get_service, verify_api_key
from schemas import BoxArea, CircleArea, OrganizationFullSchema, OrganizationSchema
from service import SecundaService


router = APIRouter(prefix="/organizations")


@router.get(
    "/all",
    description="Вывод списка всех организаций.",
    tags=["organizations"],
)
async def list_all_organizations(
    service: Annotated[SecundaService, Depends(get_service)],
    _: Annotated[str, Depends(verify_api_key)],
) -> list[OrganizationSchema]:
    return await service.list_all_organizations()


@router.get(
    "/search_in_area",
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


@router.get(
    "/{organization_id}",
    description="Вывод подробной информации о данной организации.",   
    tags=["organizations"],
)
async def get_organization(
    organization_id: Annotated[int, Path(gt=0, description="Id организации")],
    service: Annotated[SecundaService, Depends(get_service)],
    _: Annotated[str, Depends(verify_api_key)],
) -> OrganizationFullSchema:
    return await service.get_organization(organization_id)


@router.get(
    "/search_by_name",
    description="Вывод списка организаций, с названием, включающим данную подстроку.",
    tags=["organizations"],
)
async def list_organizations_by_name_search(
    search: Annotated[str, Query(min_length=1, description="Искомая подстрока")],
    service: Annotated[SecundaService, Depends(get_service)],
    _: Annotated[str, Depends(verify_api_key)],
) -> list[OrganizationSchema]:
    return await service.search_organizations_by_name(search)
