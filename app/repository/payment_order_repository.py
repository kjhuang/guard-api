"""
payment_order repository
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment_order_model import PaymentOrder
from app.repository.base_repository import BaseRepository


class PaymentOrderRepository(BaseRepository[PaymentOrder]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, PaymentOrder)
