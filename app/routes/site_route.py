"""
site route
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.auth.auth_handler import authenticate
from app.dependencies import get_site_service
from app.service.site_service import SiteService

router = APIRouter(prefix="/api/site", tags=["site"])


class Site(BaseModel):
    site_id: str
    site_name: str


@router.get("", response_model=list[Site])
async def read_items(
    service: SiteService = Depends(get_site_service),
    auth: dict = Depends(authenticate),
):
    sites = await service.get_sites()
    return sites
