"""
repair_order schema
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, computed_field, field_serializer

from app.schemas.site_schema import Site

REGIONS = {"public": "公共區", "personal": "個人居家"}

ITEM_TYPES = {
    "illumination": "照明",
    "elevator": "電梯",
    "access_control": "門禁",
    "water_leak": "漏水",
}

RESERVATION_BYS = {"assistance": "管制室協助", "self": "自行預約"}

STATUS = {
    "init": "尚未處理",
    "reserved": "已預約",
    "processing": "師傅處理中",
    "done": "維修完畢",
}


class RegionValue(str, Enum):
    locals().update({k: k for k, _ in REGIONS.items()})


class ItemTypeValue(str, Enum):
    locals().update({k: k for k, _ in ITEM_TYPES.items()})


class ReservationByValue(str, Enum):
    locals().update({k: k for k, _ in RESERVATION_BYS.items()})


class StatusValue(str, Enum):
    locals().update({k: k for k, _ in STATUS.items()})


class RepairOrderBase(BaseModel):
    site_id: str
    applicant: str
    region: RegionValue  # Literal[tuple(REGIONS.keys())]
    item_type: ItemTypeValue
    description: str | None = None
    designated_service: str | None = None
    reservation_by: ReservationByValue
    # appointment_time: str | None = None


class RepairOrderCreate(RepairOrderBase):
    appointment_time: int | None = None


class RepairOrderUpdate(BaseModel):
    # site_id: str | None = None
    # applicant: str | None = None
    # region: str | None = None
    # item_type: str | None = None
    # description: str | None = None
    # designated_service: str | None = None
    # reservation_by: str | None = None
    # appointment_time: str | None = None
    status: str


class RepairOrder(RepairOrderBase):
    id: str
    appointment_time: datetime | None = None
    status: StatusValue
    created_at: str | datetime = None
    created_by: str | None = None

    model_config = ConfigDict(from_attributes=True)


class LookupValue(BaseModel):
    id: str
    value: str


class RepairOrderView(RepairOrder):
    site_id: str = Field(..., exclude=True)

    site: Site | None = None

    @field_serializer("appointment_time")
    def format_appointment_time(self, value: datetime | None) -> str | None:
        if value is None:
            return None
        return value.strftime("%Y/%m/%d %H:%M:%S")

    @computed_field
    def appointment_ts(self) -> int:
        return int(self.appointment_time.timestamp()) if self.appointment_time else 0

    @field_serializer("region")
    def format_region(self, region: str | None) -> LookupValue | None:
        if region is None:
            return None
        return LookupValue(id=region, value=REGIONS[region])

    @field_serializer("item_type")
    def format_item_type(self, item_type: str | None) -> LookupValue | None:
        if item_type is None:
            return None
        return LookupValue(id=item_type, value=ITEM_TYPES[item_type])

    @field_serializer("reservation_by")
    def format_reservation_by(self, reservation_by: str | None) -> LookupValue | None:
        if reservation_by is None:
            return None
        return LookupValue(id=reservation_by, value=RESERVATION_BYS[reservation_by])

    @field_serializer("status")
    def format_status(self, status: str | None) -> LookupValue | None:
        if status is None:
            return None
        return LookupValue(id=status, value=STATUS[status])
