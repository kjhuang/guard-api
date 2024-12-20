"""
payment_order schema
"""

from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


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
    status: str = Field(max_length=20)
    created_at: datetime | None = None
    created_by: Optional[str] = Field(None, max_length=64)
    # site: Optional[Site] = None
    # building: Optional[Building] = None
    model_config = ConfigDict(from_attributes=True)
