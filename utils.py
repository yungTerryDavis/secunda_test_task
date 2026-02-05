from collections.abc import Sequence
from math import asin, cos, radians, sin, sqrt

from constants import EARTH_RADIUS as R
from models import Building
from schemas import BoxArea, CircleArea


def distance_wgs84(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * R * asin(sqrt(a))


def find_buildings_in_box_area(buildings: Sequence[Building], area: BoxArea) -> list[Building]:
    res: list[Building] = []
    for b in buildings:
        b_lat = float(b.coordinates.split(",")[0])
        b_lon = float(b.coordinates.split(",")[1])
        if (
            abs(area.lat1 - b_lat) <= abs(area.lat1 - area.lat2)
            and abs(area.lon1 - b_lon) <= abs(area.lon1 - area.lon2)
        ):
            res.append(b)
    return res


def find_buildings_in_circle_area(buildings: Sequence[Building], area: CircleArea) -> list[Building]:
    res: list[Building] = []
    for b in buildings:
        if (
            distance_wgs84(
                float(b.coordinates.split(",")[0]),
                float(b.coordinates.split(",")[1]),
                area.lat,
                area.lon,
            ) <= area.radius
        ):
            res.append(b)
    return res
