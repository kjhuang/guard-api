"""
announce route
"""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, File, Form, HTTPException, UploadFile

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
        site_id=site_id, title=title, severity=severity, content_file=file
    )

    return await service.create(announce_create)


@router.get("/{announce_id}", response_model=announce_schema.AnnounceView | None)
async def read_announce(
    announce_id: str, service: AnnounceService = Depends(get_announce_service)
):
    return await service.get_by_keys(id=announce_id)


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
    announce_update = announce_schema.AnnounceUpdate(
        **update_data.content.model_dump(exclude_unset=True), content_file=file
    )
    return await service.update(announce_update, id=announce_id)


@router.get("", response_model=list[announce_schema.AnnounceView])
async def read_announces(
    site_id: str | None = None,
    service: AnnounceService = Depends(get_announce_service),
    auth: dict = Depends(authenticate),
):
    filters = {}
    if site_id:
        filters[("site_id", "=")] = site_id
    announces = await service.query(filters=filters)
    return announces


@router.delete("/{announce_id}", status_code=204)
async def delete_announce(
    announce_id: str, service: AnnounceService = Depends(get_announce_service)
):
    """
    Delete a announce by ID.
    """
    try:
        await service.delete_by_keys(id=announce_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
