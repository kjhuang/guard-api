"""
building route
"""

from fastapi import APIRouter, Depends

import app.schemas.building_schema as building_schema
from app.auth.auth_handler import authenticate
from app.dependencies import get_building_service
from app.service.building_service import BuildingService

router = APIRouter(prefix="/api/building", tags=["building"])


@router.get("", response_model=list[building_schema.SiteBuildingView])
async def read_buildings(
    site_id: str | None = None,
    service: BuildingService = Depends(get_building_service),
    auth: dict = Depends(authenticate),
):
    site_buildings = await service.get_buildings(site_id)
    return site_buildings
