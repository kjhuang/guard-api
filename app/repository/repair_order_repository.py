"""
repair_order repository
"""

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.repair_order_model import RepairOrder
from app.repository.base_repository import BaseRepository


class RepairOrderRepository(BaseRepository[RepairOrder]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, RepairOrder)

    async def get_repair_order(self, repair_order_id: str) -> RepairOrder | None:
        repair_order = await self.get_by_keys(
            load_options=[joinedload(RepairOrder.site)], id=repair_order_id
        )
        return repair_order

    async def get_repair_orders(
        self,
        site_id: str | None = None,
        start_appointment_time: int | None = None,
        end_appointment_time: int | None = None,
    ) -> list[RepairOrder]:
        filters = {}
        if site_id:
            filters[("site_id", "==")] = site_id
        if start_appointment_time:
            filters[("appointment_time", ">=")] = datetime.fromtimestamp(
                start_appointment_time
            )
        if end_appointment_time:
            filters[("appointment_time", "<=")] = datetime.fromtimestamp(
                end_appointment_time
            )
        repair_orders = await self.query(
            load_options=[joinedload(RepairOrder.site)], filters=filters
        )
        return repair_orders
