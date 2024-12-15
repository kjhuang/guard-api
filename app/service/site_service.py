"""
site service
"""

import app.schemas.site_schema as site_schema
from app.db.unit_of_work import AsyncUnitOfWork
from app.repository.site_repository import SiteRepository


class SiteService:
    def __init__(self, uow: AsyncUnitOfWork):
        self.uow = uow

    async def get_sites(self) -> list[site_schema.Site]:
        async with self.uow as uow:
            site_repo = SiteRepository(uow.session)
            sites = await site_repo.get_all()

            return [site_schema.Site.model_validate(site) for site in sites]
