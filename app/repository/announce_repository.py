"""
announce repository
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.announce_model import Announce
from app.repository.base_repository import BaseRepository


class AnnounceRepository(BaseRepository[Announce]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Announce)
