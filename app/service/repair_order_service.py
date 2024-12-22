"""
repair_order service
"""

import uuid
from datetime import datetime

import app.schemas.repair_order_schema as repair_order_schema
from app.db.unit_of_work import AsyncUnitOfWork
from app.models.repair_order_model import RepairOrder
from app.repository.repair_order_repository import RepairOrderRepository
from app.service.base_service import BaseService


class RepairOrderService(
    BaseService[
        RepairOrder,
        repair_order_schema.RepairOrderCreate,
        repair_order_schema.RepairOrderUpdate,
        repair_order_schema.RepairOrder,
        repair_order_schema.RepairOrderView,
    ]
):
    repository = RepairOrderRepository
    output_schema = repair_order_schema.RepairOrder
    query_schema = repair_order_schema.RepairOrderView
    relation_strategies = {"basic": ["site"], "full": ["site"]}

    def __init__(self, uow: AsyncUnitOfWork):
        super().__init__(uow)

    async def prepare_create_data(
        self, repair_order_create: repair_order_schema.RepairOrderCreate
    ) -> RepairOrder:
        """
        Custom data preparation: add extra fields or transformations.
        """
        reserved_at: datetime | None = None
        if repair_order_create.appointment_time:
            # reserved_at = datetime.strptime(
            #     repair_order_create.appointment_time, "%Y/%m/%d %H:%M"
            # )
            reserved_at = datetime.fromtimestamp(repair_order_create.appointment_time)

        payment_order = RepairOrder(
            id=str(uuid.uuid4()),
            **repair_order_create.model_dump(exclude={"appointment_time"}),
            appointment_time=reserved_at,
            status="init",
            created_at=datetime.now(),
            created_by="",
        )
        return payment_order
