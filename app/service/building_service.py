"""
building service
"""

import app.schemas.building_schema as building_schema
from app.db.unit_of_work import AsyncUnitOfWork
from app.repository.building_repository import BuildingRepository


class BuildingService:
    def __init__(self, uow: AsyncUnitOfWork):
        self.uow = uow

    async def get_buildings(self, site_id: str | None) -> list[building_schema.BuildingView]:
        async with self.uow as uow:
            building_repo = BuildingRepository(uow.session)
            buildings = await building_repo.get_buildings(site_id)

            return [building_schema.BuildingView.model_validate(building) for building in buildings]
