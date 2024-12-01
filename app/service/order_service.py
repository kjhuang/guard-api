"""
order service
"""

import app.schemas.order_schema as order_schema
from app.db.unit_of_work import AsyncUnitOfWork
from app.repository.order_repository import OrderRepository


class OrderService:
    def __init__(self, uow: AsyncUnitOfWork):
        self.uow = uow

    async def get_order(self, user_id: int, order_id: int) -> order_schema.Order:
        """
        Retrieve an order by compound primary keys (user_id and order_id).
        """
        async with self.uow as uow:
            order_repo = OrderRepository(uow.session)
            order = await order_repo.get_by_keys(user_id=user_id, order_id=order_id)
            if not order:
                raise ValueError("Order not found")
            return order_schema.Order.model_validate(order)

    async def update_order(
        self, user_id: int, order_id: int, update_data: dict
    ) -> order_schema.Order:
        async with self.uow as uow:
            order_repo = OrderRepository(uow.session)
            updated_order = await order_repo.update(
                update_data, user_id=user_id, order_id=order_id
            )
            if not updated_order:
                raise ValueError("Order not found")
            return order_schema.Order.model_validate(updated_order)
