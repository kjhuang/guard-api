"""
item route
"""

from fastapi import APIRouter, Depends, HTTPException

import app.schemas.item_schema as item_schema
from app.auth.auth_handler import authenticate
from app.dependencies import get_item_service
from app.service.item_service import ItemService

router = APIRouter(prefix="/api/items", tags=["items"])


# CRUD operations
@router.post("/")
async def create_item(
    item_create: item_schema.ItemCreate,
    service: ItemService = Depends(get_item_service),
    auth: dict = Depends(authenticate),
) -> item_schema.Item:
    result = await service.create(item_create)
    return result


@router.get("/{item_id}", response_model=item_schema.Item | None)
async def read_item(item_id: str, service: ItemService = Depends(get_item_service)):
    return await service.get_by_keys(id=item_id)


@router.get("/", response_model=list[item_schema.Item])
async def read_items(
    skip: int = 0,
    limit: int = 10,
    service: ItemService = Depends(get_item_service),
    auth: dict = Depends(authenticate),
):
    items = await service.query()
    return items


@router.patch("/{item_id}")
async def update_item(
    item_id: str,
    item_update: item_schema.ItemUpdate,
    service: ItemService = Depends(get_item_service),
) -> item_schema.Item:
    """
    Update item
    """
    try:
        result = await service.update(item_update, id=item_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: str, service: ItemService = Depends(get_item_service)):
    """
    Delete a item by ID.
    """
    try:
        await service.delete_by_keys(id=item_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
