"""
site route
"""

from fastapi import APIRouter, Depends

import app.schemas.site_schema as site_schema
from app.auth.auth_handler import authenticate
from app.dependencies import get_site_service
from app.service.site_service import SiteService

router = APIRouter(prefix="/api/site", tags=["site"])


@router.get("", response_model=list[site_schema.Site])
async def read_sites(
    service: SiteService = Depends(get_site_service),
    auth: dict = Depends(authenticate),
):
    sites = await service.get_sites()
    return sites
