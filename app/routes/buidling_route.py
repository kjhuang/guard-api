"""
building route
"""

from fastapi import APIRouter, Depends

from app.auth.auth_handler import authenticate
from app.dependencies import get_building_service
from app.schemas.building_schema import BuildingView
from app.service.building_service import BuildingService

router = APIRouter(prefix="/api/building", tags=["building"])


@router.get("", response_model=list[BuildingView])
async def read_buildings(
    site_id: str | None = None,
    service: BuildingService = Depends(get_building_service),
    auth: dict = Depends(authenticate),
):
    buildings = await service.get_buildings(site_id)
    return buildings
