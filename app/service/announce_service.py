"""
announce service
"""

import uuid
from datetime import datetime

import app.schemas.announce_schema as announce_schema
from app.db.unit_of_work import AsyncUnitOfWork
from app.models.announce_model import Announce
from app.repository.announce_repository import AnnounceRepository
from app.service.base_service import BaseService
from app.service.file_service import create_from_upload, delete_blob


class AnnounceService(
    BaseService[
        Announce,
        announce_schema.AnnounceCreate,
        announce_schema.AnnounceUpdateInput,
        announce_schema.Announce,
        announce_schema.AnnounceView,
    ]
):
    repository = AnnounceRepository
    output_schema = announce_schema.Announce
    query_schema = announce_schema.AnnounceView
    relation_strategies = {"basic": ["site"], "full": ["site"]}

    def __init__(self, uow: AsyncUnitOfWork):
        super().__init__(uow)

    async def prepare_create_data(
        self, announce_create: announce_schema.AnnounceCreate
    ) -> Announce:
        """
        Custom data preparation: add extra fields or transformations.
        """
        module_name = f"announce/{announce_create.site_id}"
        object_name = await create_from_upload(
            announce_create.content_file, module_name
        )
        announce = Announce(
            id=str(uuid.uuid4()),
            content_path=object_name,
            publish_date=datetime.now(),
            **announce_create.model_dump(exclude={"content_file"}),
        )
        return announce

    async def prepare_update_data(
        self, update_data: announce_schema.AnnounceUpdate, obj: Announce
    ) -> dict:
        data = update_data.model_dump(exclude_unset=True, exclude={"content_file"})

        if update_data.content_file:
            if obj.content_path:
                await delete_blob(obj.content_path)
            site_id = update_data.site_id if update_data.site_id else obj.site_id
            module_name = f"announce/{site_id}"
            object_name = await create_from_upload(
                update_data.content_file, module_name
            )
            data["content_path"] = object_name

        return data

    async def post_delete_hook(self, obj: Announce):
        """Post-delete hook for additional logic."""
        if obj.content_path:
            await delete_blob(obj.content_path)
