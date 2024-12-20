"""
building repository
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.models.building_model import Building
from app.repository.base_repository import BaseRepository


class BuildingRepository(BaseRepository[Building]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Building)

    async def get_buildings(self, site_id: str | None = None) -> list[Building]:
        stmt = select(Building).options(joinedload(Building.site))
        if site_id:
            stmt = stmt.where(Building.site_id == site_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
