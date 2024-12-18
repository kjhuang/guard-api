"""
repair_order service
"""

import uuid
from datetime import datetime

import app.schemas.repair_order_schema as repair_order_schema
from app.db.unit_of_work import AsyncUnitOfWork
from app.models.repair_order_model import RepairOrder
from app.repository.repair_order_repository import RepairOrderRepository


class RepairOrderService:
    def __init__(self, uow: AsyncUnitOfWork):
        self.uow = uow

    async def create_repair_order(
        self,
        repair_order_create: repair_order_schema.RepairOrderCreate,
    ) -> repair_order_schema.RepairOrder:
        async with self.uow as uow:
            repair_order_repo = RepairOrderRepository(uow.session)
            new_repair_order = RepairOrder(
                id=str(uuid.uuid4()),
                **repair_order_create.model_dump(),
                created_at=datetime.now(),
                created_by="",
            )
            print("new_repair_order:", new_repair_order)
            await repair_order_repo.create(new_repair_order)
            return repair_order_schema.RepairOrder.model_validate(new_repair_order)

    async def get_repair_order(
        self, repair_order_id: str
    ) -> repair_order_schema.RepairOrder:
        async with self.uow as uow:
            repair_order_repo = RepairOrderRepository(uow.session)
            repair_order = await repair_order_repo.get_by_keys(id=repair_order_id)
            if not repair_order:
                raise ValueError("Item not found")
            return repair_order_schema.RepairOrder.model_validate(repair_order)

    async def get_repair_orders(self) -> list[repair_order_schema.RepairOrder]:
        async with self.uow as uow:
            repair_order_repo = RepairOrderRepository(uow.session)
            repair_orders = await repair_order_repo.get_all()

            return [
                repair_order_schema.RepairOrder.model_validate(repair_order)
                for repair_order in repair_orders
            ]

    async def update_repair_order(
        self,
        repair_order_id: str,
        repair_order_update: repair_order_schema.RepairOrderUpdate,
    ) -> repair_order_schema.RepairOrder:
        """
        Update repair_order
        """
        async with self.uow as uow:
            repair_order_repo = RepairOrderRepository(uow.session)
            updated_repair_order = await repair_order_repo.update(
                repair_order_update.dict(exclude_unset=True), id=repair_order_id
            )
            if not updated_repair_order:
                raise ValueError("Item not found")
            return repair_order_schema.RepairOrder.model_validate(updated_repair_order)

    async def delete_repair_order(self, repair_order_id: str):
        """
        Delete a repair_order by id
        """
        async with self.uow as uow:
            repair_order_repo = RepairOrderRepository(uow.session)
            repair_order = await repair_order_repo.get_by_keys(id=repair_order_id)
            if not repair_order:
                raise ValueError("User not found")
            await repair_order_repo.delete_obj(repair_order)
