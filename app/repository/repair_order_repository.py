"""
repair_order repository
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.models.repair_order_model import RepairOrder
from app.repository.base_repository import BaseRepository


class RepairOrderRepository(BaseRepository[RepairOrder]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, RepairOrder)

    async def get_repair_order(self, repair_order_id: str) -> RepairOrder | None:
        result = await self.session.execute(
            select(RepairOrder)
            .options(joinedload(RepairOrder.site))
            .where(RepairOrder.id == repair_order_id)
        )
        return result.scalar_one_or_none()

    async def get_repair_orders(self, site_id: str | None = None) -> list[RepairOrder]:
        stmt = select(RepairOrder).options(joinedload(RepairOrder.site))
        if site_id:
            stmt = stmt.where(RepairOrder.site_id == site_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
