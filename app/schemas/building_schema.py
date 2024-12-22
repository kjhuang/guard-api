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


class BuildingFull(Building):
    site_id: str = Field(..., exclude=True)
    site: Site | None = None


class BuildingView(BaseModel):
    building_id: str
    building_name: str


class SiteBuildingView(BaseModel):
    site: Site
    buildings: list[BuildingView]
