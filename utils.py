from math import asin, cos, radians, sin, sqrt

from sqlalchemy import ScalarResult

from constants import EARTH_RADIUS as R
from models import Building
from schemas import BoxArea, CircleArea


def distance_wgs84(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * R * asin(sqrt(a))


def find_building_scalars_in_box_area(scalars: ScalarResult[Building], area: BoxArea) -> list[Building]:
    res: list[Building] = []
    for s in scalars:
        s_lat = float(s.coordinates.split(",")[0])
        s_lon = float(s.coordinates.split(",")[1])
        if (
            abs(area.lat1 - s_lat) <= abs(area.lat1 - area.lat2)
            and abs(area.lon1 - s_lon) <= abs(area.lon1 - area.lon2)
        ):
            res.append(s)
    return res


def find_building_scalars_in_circle_area(scalars: ScalarResult[Building], area: CircleArea) -> list[Building]:
    res: list[Building] = []
    for s in scalars:
        if (
            distance_wgs84(
                float(s.coordinates.split(",")[0]),
                float(s.coordinates.split(",")[1]),
                area.lat,
                area.lon,
            ) <= area.radius
        ):
            res.append(s)
    return res
