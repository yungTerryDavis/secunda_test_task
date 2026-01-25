from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import Base
from models import Building, Organization, Practice


async def get_objects_count(session: AsyncSession, model: type[Base]) -> int:
    stmt = select(func.count()).select_from(model)
    return await session.scalar(stmt) or 0


class Repository:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def list_buildings(self):
        stmt = select(Building)
        return (await self._session.scalars(stmt)).all()

    async def list_organizations(self):
        stmt = (
            select(Organization)
            .options(selectinload(Organization.practices))
        )
        return (await self._session.scalars(stmt)).all()

    async def list_practices(self):
        stmt = (
            select(Practice)
            .options(selectinload(Practice.organizations))
        )
        return (await self._session.scalars(stmt)).all()

    async def list_organizations_by_building_ids(self, building_ids: list[int]):
        stmt = (
            select(Organization)
            .where(Organization.building_id.in_(building_ids))
            .options(selectinload(Organization.practices))
        )
        return (await self._session.scalars(stmt)).all()

    async def list_organizations_by_practice_id(self, practice_id: int):
        stmt = (
            select(Organization)
            .where(
                Organization.practices.any(Practice.id == practice_id)
            )
            .options(
                selectinload(Organization.practices)
            )
        )
        return (await self._session.scalars(stmt)).all()

    async def get_organization(self, organization_id: int):
        stmt = (
            select(Organization)
            .where(Organization.id == organization_id)
            .options(
                selectinload(Organization.practices),
                selectinload(Organization.building)
            )
        )
        return await self._session.scalar(stmt)

    async def list_organizations_by_practice_id_recursively(self, practice_id: int):
        stmt = (
            select(Organization)
            .join(Organization.practices)
            .where(
                or_(
                    Practice.id == practice_id,
                    Practice.parent_id == practice_id,
                    Practice.parent.has(parent_id=practice_id)
                )
            )
            .distinct()
            .options(selectinload(Organization.practices))
        )
        return (await self._session.scalars(stmt)).all()

    async def list_organizations_by_name_search(self, search_substr: str):
        stmt = (
            select(Organization)
            .where(Organization.name.ilike(f"%{search_substr}%"))
            .options(selectinload(Organization.practices))
        )
        return (await self._session.scalars(stmt)).all()
