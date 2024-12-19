"""
item route
"""

from fastapi import APIRouter, Depends, HTTPException

import app.schemas.item_schema as item_schema
from app.auth.auth_handler import authenticate
from app.dependencies import get_item_service, get_item_service2
from app.service.item_service import ItemService, ItemService2
from app.service.service_middleware import service_middleware

router = APIRouter(prefix="/api/items", tags=["items"])


# CRUD operations
@router.post("/")
async def create_item(
    item_create: item_schema.ItemCreate,
    service: ItemService2 = Depends(get_item_service2),
    auth: dict = Depends(authenticate),
) -> item_schema.Item:
    # return await service.create_item(item_create)
    result = await service_middleware(service, "create", item_create)
    return result


@router.get("/{item_id}", response_model=item_schema.Item)
async def read_item(item_id: str, service: ItemService = Depends(get_item_service)):
    return await service.get_item(item_id)


@router.get("/", response_model=list[item_schema.Item])
async def read_items(
    skip: int = 0,
    limit: int = 10,
    service: ItemService = Depends(get_item_service),
    auth: dict = Depends(authenticate),
):
    items = await service.get_items()
    return items


@router.patch("/{item_id}")
async def update_item(
    item_id: str,
    item_update: item_schema.ItemUpdate,
    service: ItemService2 = Depends(get_item_service2),
) -> item_schema.Item:
    """
    Update item
    """
    try:
        # return await service.update_item(item_id, item_update)
        result = await service_middleware(service, "update", item_update, id=item_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: str, service: ItemService = Depends(get_item_service)):
    """
    Delete a item by ID.
    """
    try:
        await service.delete_item(item_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
