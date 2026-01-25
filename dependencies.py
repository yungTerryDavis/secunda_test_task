from typing import Annotated

from fastapi import Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_422_UNPROCESSABLE_CONTENT

from database import get_db_session
from repository import Repository
from schemas import BoxArea, CircleArea
from service import SecundaService


# -------------- Service --------------
def get_service(session: Annotated[AsyncSession, Depends(get_db_session)]):
    repo = Repository(session)
    return SecundaService(repo)

# -------------- Query Params --------------
def box_query(
    lat1: Annotated[float | None, Query(ge=-90, le=90)] = None,
    lon1: Annotated[float | None, Query(ge=-180, le=180)] = None,
    lat2: Annotated[float | None, Query(ge=-90, le=90)] = None,
    lon2: Annotated[float | None, Query(ge=-180, le=180)] = None,
) -> BoxArea | None:
    if None in (lat1, lon1, lat2, lon2):
        return None
    return BoxArea(lat1=lat1, lon1=lon1, lat2=lat2, lon2=lon2)  # pyright: ignore[reportArgumentType]


def circle_query(
    lat: Annotated[float | None, Query(ge=-90, le=90)] = None,
    lon: Annotated[float | None, Query(ge=-180, le=180)] = None,
    radius: Annotated[float | None, Query(ge=0)] = None,
) -> CircleArea | None:
    if None in (lat, lon, radius):
        return None
    return CircleArea(lat=lat, lon=lon, radius=radius)  # pyright: ignore[reportArgumentType]


def area_query(
    box: Annotated[BoxArea | None, Depends(box_query)],
    circle: Annotated[CircleArea | None, Depends(circle_query)],
) -> BoxArea | CircleArea | None:
    if box and circle:
        raise HTTPException(HTTP_422_UNPROCESSABLE_CONTENT, "Specify only one area")
    if not box and not circle:
        raise HTTPException(HTTP_422_UNPROCESSABLE_CONTENT, "Area is required")
    return box or circle
