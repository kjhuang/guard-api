"""
item service
"""

import uuid

import app.schemas.item_schema as item_schema
from app.db.unit_of_work import AsyncUnitOfWork
from app.models.item_model import Item
from app.repository.item_repository import ItemRepository


class ItemService:
    def __init__(self, uow: AsyncUnitOfWork):
        self.uow = uow

    async def create_item(
        self,
        item_create: item_schema.ItemCreate,
    ) -> item_schema.Item:
        async with self.uow as uow:
            item_repo = ItemRepository(uow.session)
            # new_item = Item(
            #     id=str(uuid.uuid4()),
            #     name=item_create.name,
            #     description=item_create.description,
            #     price=item_create.price,
            # )
            new_item = Item(id=str(uuid.uuid4()), **item_create.model_dump())
            await item_repo.create(new_item)
            return item_schema.Item.model_validate(new_item)

    async def get_item(self, item_id: str) -> item_schema.Item:
        async with self.uow as uow:
            item_repo = ItemRepository(uow.session)
            item = await item_repo.get_by_keys(id=item_id)
            if not item:
                raise ValueError("Item not found")
            return item_schema.Item.model_validate(item)

    async def get_items(self) -> list[item_schema.Item]:
        async with self.uow as uow:
            item_repo = ItemRepository(uow.session)
            items = await item_repo.get_all()

            return [item_schema.Item.model_validate(item) for item in items]

    async def update_item(
        self, item_id: str, user_update: item_schema.ItemUpdate
    ) -> item_schema.Item:
        """
        Update item
        """
        async with self.uow as uow:
            item_repo = ItemRepository(uow.session)
            updated_item = await item_repo.update(
                user_update.dict(exclude_unset=True), id=item_id
            )
            if not updated_item:
                raise ValueError("Item not found")
            return item_schema.Item.model_validate(updated_item)

    async def delete_item(self, item_id: str):
        """
        Delete a item by ID.
        :param item_id: ID of the item to delete.
        """
        async with self.uow as uow:
            item_repo = ItemRepository(uow.session)
            item = await item_repo.get_by_keys(id=item_id)
            if not item:
                raise ValueError("User not found")
            await item_repo.delete_obj(item)
