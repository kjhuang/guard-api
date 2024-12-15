"""
site schema
"""

from pydantic import BaseModel, ConfigDict


class Site(BaseModel):
    site_id: str
    site_name: str

    model_config = ConfigDict(from_attributes=True)
