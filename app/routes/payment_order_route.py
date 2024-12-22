"""
payment_order route
"""

from fastapi import APIRouter, Depends, HTTPException

import app.schemas.payment_order_schema as payment_order_schema
from app.auth.auth_handler import authenticate
from app.dependencies import get_payment_order_service
from app.service.payment_order_service import PaymentOrderService

router = APIRouter(prefix="/api/payment_orders", tags=["payment_orders"])


# CRUD operations
@router.post("")
async def create_payment_order(
    payment_order_create: payment_order_schema.PaymentOrderCreate,
    service: PaymentOrderService = Depends(get_payment_order_service),
    auth: dict = Depends(authenticate),
) -> payment_order_schema.PaymentOrder:
    result = await service.create(payment_order_create)
    return result


@router.get(
    "/{payment_order_id}", response_model=payment_order_schema.PaymentOrderView | None
)
async def read_payment_order(
    payment_order_id: str,
    service: PaymentOrderService = Depends(get_payment_order_service),
):
    return await service.get_by_keys(id=payment_order_id)


@router.get("", response_model=list[payment_order_schema.PaymentOrderView])
async def read_payment_orders(
    site_id: str | None = None,
    building_id: str | None = None,
    service: PaymentOrderService = Depends(get_payment_order_service),
    auth: dict = Depends(authenticate),
):
    filters = {}
    if site_id:
        filters[("site_id", "=")] = site_id
    if building_id:
        filters[("building_id", "=")] = building_id
    items = await service.query(filters=filters)
    return items


@router.patch("/{payment_order_id}")
async def update_payment_order(
    payment_order_id: str,
    payment_order_update: payment_order_schema.PaymentOrderUpdate,
    service: PaymentOrderService = Depends(get_payment_order_service),
) -> payment_order_schema.PaymentOrder:
    """
    Update payment_order
    """
    try:
        # return await service.update_item(item_id, item_update)
        result = await service.update(payment_order_update, id=payment_order_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{payment_order_id}", status_code=204)
async def delete_payment_order(
    payment_order_id: str,
    service: PaymentOrderService = Depends(get_payment_order_service),
):
    """
    Delete a payment_order by ID.
    """
    try:
        await service.delete_by_keys(id=payment_order_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
