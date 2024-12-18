"""
repair_order schema
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RepairOrderBase(BaseModel):
    applicant: str
    region: str
    item_type: str
    description: str | None = None
    designated_service: str | None = None
    reservation_by: str | None = None
    appointment_time: str | None = None


class RepairOrderCreate(RepairOrderBase):
    pass


class RepairOrderUpdate(BaseModel):
    applicant: str | None = None
    region: str | None = None
    item_type: str | None = None
    description: str | None = None
    designated_service: str | None = None
    reservation_by: str | None = None
    appointment_time: str | None = None


class RepairOrder(RepairOrderBase):
    id: str
    created_at: str | datetime = None
    created_by: str | None = None

    model_config = ConfigDict(from_attributes=True)
