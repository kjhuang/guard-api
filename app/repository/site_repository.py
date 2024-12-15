"""
site repository
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.site_model import Site
from app.repository.base_repository import BaseRepository


class SiteRepository(BaseRepository[Site]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Site)
