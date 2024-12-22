"""
announce schema
"""

import json
from datetime import datetime

from fastapi import UploadFile
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_serializer,
    model_validator,
)

import app.utils.config as config
from app.schemas.site_schema import Site


class AnnounceCreate(BaseModel):
    site_id: str
    title: str
    severity: int
    content_file: UploadFile


class AnnounceUpdateInput(BaseModel):
    site_id: str | None = None
    title: str | None = None
    severity: int | None = None


class AnnounceUpdateInputJS(BaseModel):
    content: AnnounceUpdateInput

    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class AnnounceUpdate(AnnounceUpdateInput):
    content_file: UploadFile | None = None
    content_path: str | None = None


class Announce(BaseModel):
    id: str
    site_id: str
    title: str
    severity: int
    content_path: str
    publish_date: datetime

    model_config = ConfigDict(from_attributes=True)


class AnnounceView(Announce):
    site_id: str = Field(..., exclude=True)
    content_path: str = Field(..., exclude=True)

    site: Site | None = None

    @field_serializer("publish_date")
    def format_publish_date(self, value: datetime | None) -> str | None:
        if value is None:
            return None
        return value.strftime("%Y/%m/%d %H:%M:%S")

    @computed_field
    def publish_ts(self) -> int:
        return int(self.publish_date.timestamp())

    @computed_field
    @property
    def url(self) -> str:
        return config.BLOB_URL_PREFIX + self.content_path if self.content_path else None
