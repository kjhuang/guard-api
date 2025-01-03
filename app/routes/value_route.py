"""
value route
"""

from fastapi import APIRouter, Depends

from app.auth.auth_handler import authenticate
from app.schemas.repair_order_schema import (
    ITEM_TYPES,
    REGIONS,
    REPAIR_ORDER_STATUS,
    RESERVATION_BYS,
)

router = APIRouter(prefix="/api/values", tags=["values"])


@router.get("/repair_order_form")
async def read_repair_orders(
    auth: dict = Depends(authenticate),
) -> dict[str, dict[str, str]]:
    list_items = {
        "region": REGIONS,
        "item_type": ITEM_TYPES,
        "reservation_by": RESERVATION_BYS,
        "status": REPAIR_ORDER_STATUS,
    }

    return list_items
