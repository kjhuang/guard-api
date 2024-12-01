"""
order route
"""

from fastapi import APIRouter, Depends, HTTPException

import app.schemas.order_schema as order_schema
from app.db.unit_of_work import AsyncUnitOfWork
from app.dependencies import get_async_unit_of_work, get_item_service, get_order_service
from app.service.item_service import ItemService
from app.service.order_service import OrderService

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.get("/{user_id}/{order_id}")  # Or use an OrderSchema
async def get_order(
    user_id: int,
    order_id: int,
    item_service: ItemService = Depends(get_item_service),
    order_service: OrderService = Depends(get_order_service),
) -> order_schema.Order:
    """
    Retrieve an order by user_id and order_id.
    """
    print(f"uow instance ID in user_service: {id(item_service.uow)}")
    print(f"uow instance ID in order_service: {id(order_service.uow)}")
    try:
        return await order_service.get_order(user_id, order_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{user_id}/{order_id}")
async def update_order(
    user_id: int,
    order_id: int,
    update_data: dict,
    order_service: OrderService = Depends(get_order_service),
) -> order_schema.Order:
    try:
        print("update_order...")
        order = await order_service.update_order(user_id, order_id, update_data)
        # await order_service.uow.commit()
        return order
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# @router.put("/{user_id}/{order_id}")
async def update_order2(
    user_id: int,
    order_id: int,
    update_data: dict,
    uow: AsyncUnitOfWork = Depends(get_async_unit_of_work),
) -> order_schema.Order:
    try:
        order_service = OrderService(uow)
        order = await order_service.update_order(user_id, order_id, update_data)
        # await uow.commit()
        return order
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
