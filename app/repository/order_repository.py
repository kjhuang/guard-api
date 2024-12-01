"""
order repository
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order_model import Order
from app.repository.base_repository import BaseRepository


class OrderRepository(BaseRepository[Order]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Order)
