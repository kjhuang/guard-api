"""
announce repository
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.models.announce_model import Announce
from app.repository.base_repository import BaseRepository


class AnnounceRepository(BaseRepository[Announce]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Announce)

    async def get_announce(self, announce_id: str) -> Announce | None:
        result = await self.session.execute(
            select(Announce)
            .options(joinedload(Announce.site))
            .where(Announce.id == announce_id)
        )
        return result.scalar_one_or_none()

    async def get_announces(self, site_id: str | None = None) -> list[Announce]:
        stmt = select(Announce).options(joinedload(Announce.site))
        if site_id:
            stmt = stmt.where(Announce.site_id == site_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
