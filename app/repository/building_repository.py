"""
building repository
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.building_model import Building
from app.repository.base_repository import BaseRepository


class BuildingRepository(BaseRepository[Building]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Building)

    async def get_buildings(self, site_id: str | None = None) -> list[Building]:
        filters = {}
        if site_id:
            filters[("site_id", "=")] = site_id

        order_by = {"site_id": "asc", "building_id": "asc"}
        buildings = await self.query(
            load_relations=["site"], filters=filters, order_by=order_by
        )
        return buildings
