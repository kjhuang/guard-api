"""
payment_order service
"""

import uuid
from datetime import datetime

import app.schemas.payment_order_schema as payment_order_schema
from app.db.unit_of_work import AsyncUnitOfWork
from app.models.payment_order_model import PaymentOrder
from app.repository.payment_order_repository import PaymentOrderRepository
from app.service.base_service import BaseService


class PaymentOrderService(
    BaseService[
        PaymentOrder,
        payment_order_schema.PaymentOrderCreate,
        payment_order_schema.PaymentOrderUpdate,
        payment_order_schema.PaymentOrder,
        payment_order_schema.PaymentOrderView,
    ]
):
    repository = PaymentOrderRepository
    output_schema = payment_order_schema.PaymentOrder
    query_schema = payment_order_schema.PaymentOrderView
    relation_strategies = {"basic": ["site", "building"], "full": ["site", "building"]}

    def __init__(self, uow: AsyncUnitOfWork):
        super().__init__(uow)

    async def prepare_create_data(
        self, create_data: payment_order_schema.PaymentOrderCreate
    ) -> PaymentOrder:
        """
        Custom data preparation: add extra fields or transformations.
        """
        payment_order = PaymentOrder(
            id=str(uuid.uuid4()),
            **create_data.model_dump(),
            status="0",
            created_at=datetime.now(),
            created_by="",
        )
        return payment_order
