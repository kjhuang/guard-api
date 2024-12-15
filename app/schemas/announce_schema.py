"""
announce schema
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_serializer

from app.schemas.site_schema import Site


class AnnounceInput(BaseModel):
    site_id: str
    title: str
    severity: str


class Announce(BaseModel):
    id: str
    site_id: str
    title: str
    severity: str
    content_path: str
    publish_date: datetime
    site: Site | None = None

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("publish_date")
    def format_publish_date(self, value: datetime | None) -> str | None:
        if value is None:
            return None
        return value.strftime("%Y/%m/%d %H:%M:%S")

    # @property
    # def publish_date(self) -> str | None:
    #     if self.__dict__.get("publish_date") is None:
    #         return None
    #     return self.__dict__["publish_date"].strftime("%Y/%m/%d %H:%M:%S")
