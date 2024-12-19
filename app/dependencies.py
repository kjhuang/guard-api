"""
dependencies for route
"""

from typing import AsyncGenerator

from fastapi import Depends

from app.db.database_async import AsyncSessionLocal
from app.db.unit_of_work import AsyncUnitOfWork
from app.service.announce_service import AnnounceService
from app.service.item_service import ItemService, ItemService2
from app.service.order_service import OrderService
from app.service.repair_order_service import RepairOrderService
from app.service.site_service import SiteService


async def get_async_unit_of_work() -> AsyncGenerator[AsyncUnitOfWork, None]:
    """
    Dependency to get Async Unit of Work
    """
    uow = AsyncUnitOfWork(session_factory=AsyncSessionLocal)
    try:
        yield uow
    finally:
        pass


async def get_site_service(
    uow: AsyncUnitOfWork = Depends(get_async_unit_of_work),
) -> SiteService:
    return SiteService(uow)


async def get_announce_service(
    uow: AsyncUnitOfWork = Depends(get_async_unit_of_work),
) -> AnnounceService:
    return AnnounceService(uow)


async def get_item_service(
    uow: AsyncUnitOfWork = Depends(get_async_unit_of_work),
) -> ItemService:
    return ItemService(uow)

async def get_item_service2(
    uow: AsyncUnitOfWork = Depends(get_async_unit_of_work),
) -> ItemService2:
    return ItemService2(uow)


async def get_order_service(
    uow: AsyncUnitOfWork = Depends(get_async_unit_of_work),
) -> OrderService:
    return OrderService(uow)


async def get_repair_order_service(
    uow: AsyncUnitOfWork = Depends(get_async_unit_of_work),
) -> RepairOrderService:
    return RepairOrderService(uow)
