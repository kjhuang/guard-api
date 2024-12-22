"""
dependencies for route
"""

from typing import AsyncGenerator, Callable, Type, TypeVar

from fastapi import Depends

from app.db.database_async import AsyncSessionLocal
from app.db.unit_of_work import AsyncUnitOfWork


async def get_async_unit_of_work() -> AsyncGenerator[AsyncUnitOfWork, None]:
    """
    Dependency to get Async Unit of Work
    """
    uow = AsyncUnitOfWork(session_factory=AsyncSessionLocal)
    try:
        yield uow
    finally:
        pass


# Generic Type for Services
ServiceType = TypeVar("ServiceType")


def get_service(service_class: Type[ServiceType]) -> Callable[..., ServiceType]:
    async def _get_service(
        uow: AsyncUnitOfWork = Depends(get_async_unit_of_work),
    ) -> ServiceType:
        return service_class(uow)

    return _get_service


# async def get_site_service(
#     uow: AsyncUnitOfWork = Depends(get_async_unit_of_work),
# ) -> SiteService:
#     return SiteService(uow)


# async def get_announce_service(
#     uow: AsyncUnitOfWork = Depends(get_async_unit_of_work),
# ) -> AnnounceService:
#     return AnnounceService(uow)


# async def get_item_service(
#     uow: AsyncUnitOfWork = Depends(get_async_unit_of_work),
# ) -> ItemService:
#     return ItemService(uow)


# async def get_repair_order_service(
#     uow: AsyncUnitOfWork = Depends(get_async_unit_of_work),
# ) -> RepairOrderService:
#     return RepairOrderService(uow)


# async def get_building_service(
#     uow: AsyncUnitOfWork = Depends(get_async_unit_of_work),
# ) -> BuildingService:
#     return BuildingService(uow)


# async def get_payment_order_service(
#     uow: AsyncUnitOfWork = Depends(get_async_unit_of_work),
# ) -> PaymentOrderService:
#     return PaymentOrderService(uow)
