"""
building service
"""

from typing import Dict, List

import app.schemas.building_schema as building_schema
from app.db.unit_of_work import AsyncUnitOfWork
from app.repository.building_repository import BuildingRepository


def convert_site_buildings(
    building_fulls: List[building_schema.BuildingFull],
) -> List[building_schema.SiteBuildingView]:
    site_building_map: Dict[str, building_schema.SiteBuildingView] = {}

    for building_full in building_fulls:
        if building_full.site is None:
            continue  # Skip if the site is None

        site_id = building_full.site.site_id
        building_view = building_schema.BuildingView(**building_full.model_dump())

        if site_id not in site_building_map:
            site_building_map[site_id] = building_schema.SiteBuildingView(
                site=building_full.site, buildings=[]
            )

        site_building_map[site_id].buildings.append(building_view)

    return list(site_building_map.values())


class BuildingService:
    def __init__(self, uow: AsyncUnitOfWork):
        self.uow = uow

    async def get_buildings(
        self, site_id: str | None
    ) -> list[building_schema.SiteBuildingView]:
        async with self.uow as uow:
            building_repo = BuildingRepository(uow.session)
            buildings = await building_repo.get_buildings(site_id)

            building_fulls = [
                building_schema.BuildingFull.model_validate(building)
                for building in buildings
            ]

            site_buildings = convert_site_buildings(building_fulls)
            return site_buildings
