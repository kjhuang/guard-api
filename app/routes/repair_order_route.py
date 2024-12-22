"""
repair order route
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

import app.schemas.repair_order_schema as repair_order_schema
from app.auth.auth_handler import authenticate
from app.dependencies import get_repair_order_service
from app.service.repair_order_service import RepairOrderService

router = APIRouter(prefix="/api/repair_orders", tags=["repair_orders"])


# CRUD operations
@router.post("")
async def create_repair_order(
    repair_order_create: repair_order_schema.RepairOrderCreate,
    service: RepairOrderService = Depends(get_repair_order_service),
    auth: dict = Depends(authenticate),
) -> repair_order_schema.RepairOrder:
    return await service.create(repair_order_create)


@router.get(
    "/{repair_order_id}", response_model=repair_order_schema.RepairOrderView | None
)
async def read_repair_order(
    repair_order_id: str,
    service: RepairOrderService = Depends(get_repair_order_service),
):
    return await service.get_by_keys(id=repair_order_id)


@router.get("", response_model=list[repair_order_schema.RepairOrderView])
async def read_repair_orders(
    site_id: str | None = None,
    start_appointment_time: int | None = None,
    end_appointment_time: int | None = None,
    service: RepairOrderService = Depends(get_repair_order_service),
    auth: dict = Depends(authenticate),
):
    filters = {}
    if site_id:
        filters[("site_id", "=")] = site_id
    if start_appointment_time:
        filters[("appointment_time", ">=")] = datetime.fromtimestamp(
            start_appointment_time
        )
    if end_appointment_time:
        filters[("appointment_time", "<=")] = datetime.fromtimestamp(
            end_appointment_time
        )
    repair_orders = await service.query(filters=filters)
    return repair_orders


@router.patch("/{repair_order_id}")
async def update_repair_order(
    repair_order_id: str,
    repair_order_update: repair_order_schema.RepairOrderUpdate,
    service: RepairOrderService = Depends(get_repair_order_service),
    auth: dict = Depends(authenticate),
) -> repair_order_schema.RepairOrder:
    """
    Update item
    """
    try:
        return await service.update(repair_order_update, id=repair_order_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{repair_order_id}", status_code=204)
async def delete_repair_order(
    repair_order_id: str,
    service: RepairOrderService = Depends(get_repair_order_service),
    auth: dict = Depends(authenticate),
):
    """
    Delete a repair_order by ID.
    """
    try:
        await service.delete_by_keys(id=repair_order_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
