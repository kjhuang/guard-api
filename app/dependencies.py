"""
dependencies for route
"""

from typing import AsyncGenerator

from fastapi import Depends

from app.db.database_async import AsyncSessionLocal
from app.db.unit_of_work import AsyncUnitOfWork
from app.service.item_service import ItemService
from app.service.order_service import OrderService


async def get_async_unit_of_work() -> AsyncGenerator[AsyncUnitOfWork, None]:
    """
    Dependency to get Async Unit of Work
    """
    uow = AsyncUnitOfWork(session_factory=AsyncSessionLocal)
    try:
        yield uow
    finally:
        pass


async def get_item_service(
    uow: AsyncUnitOfWork = Depends(get_async_unit_of_work),
) -> ItemService:
    return ItemService(uow)


async def get_order_service(
    uow: AsyncUnitOfWork = Depends(get_async_unit_of_work),
) -> OrderService:
    return OrderService(uow)