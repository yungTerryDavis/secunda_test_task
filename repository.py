from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import Base


async def get_objects_count(session: AsyncSession, model: type[Base]) -> int:
    stmt = select(func.count()).select_from(model)
    return await session.scalar(stmt) or 0
