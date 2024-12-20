"""
building schema
"""

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.site_schema import Site


class Building(BaseModel):
    site_id: str
    building_id: str
    building_name: str

    model_config = ConfigDict(from_attributes=True)


class BuildingView(Building):
    site_id: str = Field(..., exclude=True)
