"""
repair_order repository
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.repair_order_model import RepairOrder
from app.repository.base_repository import BaseRepository


class RepairOrderRepository(BaseRepository[RepairOrder]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, RepairOrder)
