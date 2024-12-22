"""
item service
"""

import uuid

import app.schemas.item_schema as item_schema
from app.db.unit_of_work import AsyncUnitOfWork
from app.models.item_model import Item
from app.repository.item_repository import ItemRepository
from app.service.base_service import BaseService


class ItemService(
    BaseService[
        Item,
        item_schema.ItemCreate,
        item_schema.ItemUpdate,
        item_schema.Item,
        item_schema.Item,
    ]
):
    repository = ItemRepository
    output_schema = item_schema.Item
    query_schema = item_schema.Item

    def __init__(self, uow: AsyncUnitOfWork):
        super().__init__(uow)
        # self.blob_storage = blob_storage
        # self.messaging_service = messaging_service

    async def prepare_create_data(self, create_data: item_schema.ItemCreate) -> Item:
        """
        Custom data preparation: add extra fields or transformations.
        """
        item = Item(id=str(uuid.uuid4()), **create_data.model_dump())
        # data["is_active"] = True  # Default active status
        return item
