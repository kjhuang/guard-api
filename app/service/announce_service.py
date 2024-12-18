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
from app.service.file_service import create_from_upload, delete_blob


class AnnounceService:
    def __init__(self, uow: AsyncUnitOfWork):
        self.uow = uow

    async def create_announce(
        self, announce_create: announce_schema.AnnounceCreate, content_file: UploadFile
    ) -> announce_schema.Announce:
        module_name = f"announce/{announce_create.site_id}"
        object_name = await create_from_upload(content_file, module_name)

        async with self.uow as uow:
            new_announce = Announce(
                id=str(uuid.uuid4()),
                content_path=object_name,
                publish_date=datetime.now(),
                **announce_create.model_dump(),
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

    async def update_announce(
        self,
        announce_id: str,
        announce_update_input: announce_schema.AnnounceUpdateInput,
        content_file: UploadFile | None,
    ) -> announce_schema.Announce:
        async with self.uow as uow:
            announce_update = announce_schema.AnnounceUpdate(
                **announce_update_input.model_dump(exclude_unset=True)
            )
            announce_repo = AnnounceRepository(uow.session)
            announce = await announce_repo.get_announce(announce_id)
            if not announce:
                raise ValueError("announce not found")

            if content_file:
                if announce.content_path:
                    await delete_blob(announce.content_path)
                module_name = f"announce/{announce.site_id}"
                object_name = await create_from_upload(content_file, module_name)
                announce_update.content_path = object_name

            announce = await announce_repo.update(
                announce_update.model_dump(exclude_unset=True), id=announce_id
            )

            return announce_schema.Announce.model_validate(announce)

    async def get_announces(
        self, site_id: str | None = None
    ) -> list[announce_schema.AnnounceView]:
        async with self.uow as uow:
            announce_repo = AnnounceRepository(uow.session)
            announces = await announce_repo.get_announces(site_id)

            return [
                announce_schema.AnnounceView.model_validate(announce)
                for announce in announces
            ]

    async def delete_announce(self, announce_id: str):
        """
        Delete announce by it
        """
        async with self.uow as uow:
            announce_repo = AnnounceRepository(uow.session)
            announce = await announce_repo.get_by_keys(id=announce_id)
            if not announce:
                raise ValueError("Announce not found")
            if announce.content_path:
                await delete_blob(announce.content_path)
            await announce_repo.delete_obj(announce)
