"""
announce schema
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, computed_field, field_serializer

import app.utils.config as config
from app.schemas.site_schema import Site


class AnnounceInput(BaseModel):
    site_id: str
    title: str
    severity: int


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
    @property
    def url(self) -> str:
        return config.BLOB_URL_PREFIX + self.content_path if self.content_path else None
