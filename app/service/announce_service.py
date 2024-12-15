"""
announce service
"""

import uuid
from datetime import datetime

import app.schemas.announce_schema as announce_schema
from app.db.unit_of_work import AsyncUnitOfWork
from app.models.announce_model import Announce
from app.repository.announce_repository import AnnounceRepository


class AnnounceService:
    def __init__(self, uow: AsyncUnitOfWork):
        self.uow = uow

    async def create_announce(
        self, announce_input: announce_schema.AnnounceInput, content_file_path: str
    ) -> announce_schema.Announce:
        async with self.uow as uow:
            new_announce = Announce(
                id=str(uuid.uuid4()),
                content_path=content_file_path,
                publish_date=datetime.now(),
                **announce_input.model_dump(),
            )
            announce_repo = AnnounceRepository(uow.session)
            await announce_repo.create(new_announce)
            print("new_announce:", new_announce)
            return announce_schema.Announce.model_validate(new_announce)

    async def get_announce(self, announce_id: str) -> announce_schema.Announce:
        async with self.uow as uow:
            announce_repo = AnnounceRepository(uow.session)
            announce = await announce_repo.get_announce(announce_id)
            if not announce:
                raise ValueError("Item not found")
            return announce_schema.Announce.model_validate(announce)

    async def get_announces(self) -> list[announce_schema.Announce]:
        async with self.uow as uow:
            announce_repo = AnnounceRepository(uow.session)
            announces = await announce_repo.get_announces()

            return [
                announce_schema.Announce.model_validate(announce)
                for announce in announces
            ]
