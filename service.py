from repository import Repository
from schemas import (
    BoxArea,
    BuildingSchema,
    CircleArea,
    OrganizationFullSchema,
    OrganizationSchema,
    PracticeSchema,
)
from utils import find_buildings_in_box_area, find_buildings_in_circle_area


class SecundaService:
    def __init__(self, repo: Repository):
        self._repo: Repository = repo

    async def list_all_buildings(self) -> list[BuildingSchema]:
        buildings = await self._repo.list_buildings()
        return [BuildingSchema.model_validate(b, from_attributes=True) for b in buildings]

    async def list_all_practices(self) -> list[PracticeSchema]:
        scalars = await self._repo.list_practices()
        return [PracticeSchema.model_validate(s, from_attributes=True) for s in scalars]

    async def list_all_organizations(self) -> list[OrganizationSchema]:
        scalars = await self._repo.list_organizations()
        return [OrganizationSchema.model_validate(s, from_attributes=True) for s in scalars]

    async def list_organizations_in_building(self, building_id: int) -> list[OrganizationSchema]:
        scalars = await self._repo.list_organizations_by_building_ids([building_id])
        return [OrganizationSchema.model_validate(s, from_attributes=True) for s in scalars]

    async def list_organizations_of_practice(self, practice_id: int) -> list[OrganizationSchema]:
        scalars = await self._repo.list_organizations_by_practice_id(practice_id)
        return [OrganizationSchema.model_validate(s, from_attributes=True) for s in scalars]

    async def list_buildings_in_area(self, area: BoxArea | CircleArea) -> list[BuildingSchema]:
        buildings = await self._repo.list_buildings()
        if type(area) == BoxArea:
            res = find_buildings_in_box_area(buildings, area)
        elif type(area) == CircleArea:
            res = find_buildings_in_circle_area(buildings, area)
        else:
            raise TypeError("Unsupported Area Type")
        return [BuildingSchema.model_validate(b, from_attributes=True) for b in res]

    async def list_organizations_in_area(self, area: BoxArea | CircleArea) -> list[OrganizationSchema]:
        buildings = await self._repo.list_buildings()
        if type(area) == BoxArea:
            buildings = find_buildings_in_box_area(buildings, area)
        elif type(area) == CircleArea:
            buildings = find_buildings_in_circle_area(buildings, area)
        else:
            raise TypeError("Unsupported Area Type")
        
        res = await self._repo.list_organizations_by_building_ids([b.id for b in buildings])
        return [OrganizationSchema.model_validate(o, from_attributes=True) for o in res]

    async def get_organization(self, organization_id: int) -> OrganizationFullSchema:
        scalar = await self._repo.get_organization(organization_id)
        return OrganizationFullSchema.model_validate(scalar, from_attributes=True)

    async def list_organizations_of_practice_recursively(self, practice_id: int) -> list[OrganizationSchema]:
        scalars = await self._repo.list_organizations_by_practice_id_recursively(practice_id)
        return [OrganizationSchema.model_validate(s, from_attributes=True) for s in scalars]

    async def search_organizations_by_name(self, search_substr: str) -> list[OrganizationSchema]:
        scalars = await self._repo.list_organizations_by_name_search(search_substr)
        return [OrganizationSchema.model_validate(s, from_attributes=True) for s in scalars]
