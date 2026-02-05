from fastapi import APIRouter

from routes.v1.routes_buildings import router as router_buildings
from routes.v1.routes_organizations import router as router_organizations
from routes.v1.routes_practices import router as router_practices


router = APIRouter(prefix="/v1")

router.include_router(router_buildings)
router.include_router(router_organizations)
router.include_router(router_practices)
