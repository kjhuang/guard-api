"""
announce route
"""

import os

from fastapi import APIRouter, Depends, File, Form, UploadFile

import app.schemas.announce_schema as announce_schema
from app.auth.auth_handler import authenticate
from app.dependencies import get_announce_service
from app.service.announce_service import AnnounceService

router = APIRouter(prefix="/api/announce", tags=["announce"])

UPLOAD_DIR = "./uploads"


@router.post("/")
async def create_announcement(
    site_id: str = Form(...),
    title: str = Form(...),
    severity: str = Form(...),
    file: UploadFile = File(...),
    service: AnnounceService = Depends(get_announce_service),
    auth: dict = Depends(authenticate),
) -> announce_schema.Announce:
    # Ensure the directory to save files exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    # Save the uploaded file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    announce_input = announce_schema.AnnounceInput(
        site_id=site_id, title=title, severity=severity
    )

    return await service.create_announce(announce_input, file_path)


@router.get("/{announce_id}", response_model=announce_schema.Announce)
async def read_announce(
    announce_id: str, service: AnnounceService = Depends(get_announce_service)
):
    return await service.get_announce(announce_id)


@router.get("/", response_model=list[announce_schema.Announce])
async def read_announces(
    service: AnnounceService = Depends(get_announce_service),
    auth: dict = Depends(authenticate),
):
    announces = await service.get_announces()
    return announces
