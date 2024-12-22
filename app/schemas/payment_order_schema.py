"""
payment_order schema
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from app.schemas.building_schema import BuildingView
from app.schemas.common_schema import LookupValue
from app.schemas.site_schema import Site

PAYMENT_ORDER_STATUS = {"0": "未繳", "1": "已繳"}


class PaymentOrderStatusValue(str, Enum):
    locals().update({k: k for k, _ in PAYMENT_ORDER_STATUS.items()})


class PaymentOrderBase(BaseModel):
    site_id: str = Field(max_length=64)
    building_id: str = Field(max_length=64)
    house_no: str = Field(max_length=60)
    house_owner: str = Field(max_length=60)
    payment_item: str = Field(max_length=60)
    amount: int = Field(ge=0)
    payment_due_date: str = Field(max_length=20)


class PaymentOrderCreate(PaymentOrderBase):
    pass


class PaymentOrderUpdate(BaseModel):
    status: str


class PaymentOrder(PaymentOrderBase):
    id: str = Field(max_length=64)
    status: PaymentOrderStatusValue
    created_at: datetime | None = None
    created_by: Optional[str] = Field(None, max_length=64)
    model_config = ConfigDict(from_attributes=True)


class PaymentOrderView(PaymentOrder):
    site_id: str = Field(exclude=True)
    building_id: str = Field(exclude=True)

    site: Site
    building: BuildingView

    @field_serializer("status")
    def format_status(self, status: str | None) -> LookupValue | None:
        if status is None:
            return None
        return LookupValue(id=status, value=PAYMENT_ORDER_STATUS[status])
