"""
announce service
"""

import uuid
from datetime import datetime

from fastapi import UploadFile

import app.schemas.announce_schema as announce_schema
from app.db.unit_of_work import AsyncUnitOfWork
from app.models.announce_model import Announce
from app.repository.announce_repository import AnnounceRepository
from app.service.file_service import create_from_upload


class AnnounceService:
    def __init__(self, uow: AsyncUnitOfWork):
        self.uow = uow

    async def create_announce(
        self, announce_input: announce_schema.AnnounceInput, content_file: UploadFile
    ) -> announce_schema.Announce:
        module_name = f"announce/{announce_input.site_id}"
        object_name = await create_from_upload(content_file, module_name)

        async with self.uow as uow:
            new_announce = Announce(
                id=str(uuid.uuid4()),
                content_path=object_name,
                publish_date=datetime.now(),
                **announce_input.model_dump(),
            )
            announce_repo = AnnounceRepository(uow.session)
            await announce_repo.create(new_announce)
            print("new_announce:", new_announce)
            return announce_schema.Announce.model_validate(new_announce)

    async def get_announce(self, announce_id: str) -> announce_schema.AnnounceView:
        async with self.uow as uow:
            announce_repo = AnnounceRepository(uow.session)
            announce = await announce_repo.get_announce(announce_id)
            if not announce:
                raise ValueError("announce not found")
            return announce_schema.AnnounceView.model_validate(announce)

    async def get_announces(self) -> list[announce_schema.AnnounceView]:
        async with self.uow as uow:
            announce_repo = AnnounceRepository(uow.session)
            announces = await announce_repo.get_announces()

            return [
                announce_schema.AnnounceView.model_validate(announce)
                for announce in announces
            ]
