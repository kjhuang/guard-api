"""
item repository
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item_model import Item
from app.repository.base_repository import BaseRepository


class ItemRepository(BaseRepository[Item]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Item)
