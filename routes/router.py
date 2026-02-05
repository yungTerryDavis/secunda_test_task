from fastapi import APIRouter

from routes.v1.router import router as router_v1


router = APIRouter(prefix="/api")
router.include_router(router_v1)
