from pydantic import BaseModel


# ----------- Building -----------
class BuildingSchema(BaseModel):
    id: int
    address: str
    coordinates: str


# ----------- Organization -----------
class OrganizationSchema(BaseModel):
    id: int
    name: str
    phone_numbers: list[str]
    building_id: int
    practices: list[PracticeShortSchema]


class OrganizationShortSchema(BaseModel):
    id: int
    name: str


class OrganizationFullSchema(BaseModel):
    id: int
    name: str
    phone_numbers: list[str]
    building: BuildingSchema
    practices: list[PracticeShortSchema]


# ----------- Practice -----------
class PracticeSchema(BaseModel):
    id: int
    name: str
    parent_id: int | None
    level: int
    organizations: list[OrganizationShortSchema]


class PracticeShortSchema(BaseModel):
    id: int
    name: str


# ----------- Query Schema -----------
class BoxArea(BaseModel):
    lat1: float
    lon1: float
    lat2: float
    lon2: float


class CircleArea(BaseModel):
    lat: float
    lon: float
    radius: float
