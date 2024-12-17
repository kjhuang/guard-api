"""
announce route
"""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, File, Form, UploadFile

import app.schemas.announce_schema as announce_schema
from app.auth.auth_handler import authenticate
from app.dependencies import get_announce_service
from app.service.announce_service import AnnounceService

router = APIRouter(prefix="/api/announce", tags=["announce"])


@router.post("")
async def create_announcement(
    site_id: str = Form(...),
    title: str = Form(...),
    severity: int = Form(...),
    file: UploadFile = File(...),
    service: AnnounceService = Depends(get_announce_service),
    auth: dict = Depends(authenticate),
) -> announce_schema.Announce:
    announce_create = announce_schema.AnnounceCreate(
        site_id=site_id, title=title, severity=severity
    )

    return await service.create_announce(announce_create, file)


@router.get("/{announce_id}", response_model=announce_schema.AnnounceView)
async def read_announce(
    announce_id: str, service: AnnounceService = Depends(get_announce_service)
):
    return await service.get_announce(announce_id)


@router.patch("/{announce_id}")
async def update_announce(
    announce_id: str,
    update_data: announce_schema.AnnounceUpdateInputJS = Body(...),
    file: Annotated[UploadFile | None, File(...)] = None,
    service: AnnounceService = Depends(get_announce_service),
    auth: dict = Depends(authenticate),
) -> announce_schema.Announce:
    """
    Update announce
    """
    return await service.update_announce(announce_id, update_data.content, file)


@router.get("", response_model=list[announce_schema.AnnounceView])
async def read_announces(
    service: AnnounceService = Depends(get_announce_service),
    auth: dict = Depends(authenticate),
):
    announces = await service.get_announces()
    return announces
