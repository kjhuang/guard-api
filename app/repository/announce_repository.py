"""
announce repository
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.announce_model import Announce
from app.repository.base_repository import BaseRepository


class AnnounceRepository(BaseRepository[Announce]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Announce)

    async def get_announce(self, announce_id: str) -> Announce | None:
        announce = await self.get_by_keys(
            load_options=[joinedload(Announce.site)], id=announce_id
        )
        return announce

    async def get_announces(self, site_id: str | None = None) -> list[Announce]:
        filters = {}
        if site_id:
            filters[("site_id", "==")] = site_id
        announces = await self.query(
            load_options=[joinedload(Announce.site)], filters=filters
        )
        return announces
