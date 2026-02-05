from typing import Annotated

from fastapi import APIRouter, Depends, Path

from dependencies import get_service, verify_api_key
from schemas import PracticeSchema, OrganizationSchema
from service import SecundaService


router = APIRouter(prefix="/practices")


@router.get(
    "/all",
    description="Вывод списка всех деятельностей.",
    tags=["practices"],
)
async def list_all_practices(
    service: Annotated[SecundaService, Depends(get_service)],
    _: Annotated[str, Depends(verify_api_key)],
) -> list[PracticeSchema]:
    return await service.list_all_practices()


@router.get(
    "/{practice_id}/organizations",
    description="Вывод списка всех организаций, занятых данным видом деятельности.",
    tags=["organizations"],
)
async def list_organizations_of_practice(
    practice_id: Annotated[int, Path(gt=0, description="Id деятельности")],
    service: Annotated[SecundaService, Depends(get_service)],
    _: Annotated[str, Depends(verify_api_key)],
) -> list[OrganizationSchema]:
    return await service.list_organizations_of_practice(practice_id)


@router.get(
    "/{practice_id}/organizations/recursive",
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
