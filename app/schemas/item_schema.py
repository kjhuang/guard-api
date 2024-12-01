"""
item schema
"""

from pydantic import BaseModel, ConfigDict


class ItemBase(BaseModel):
    name: str
    description: str
    price: int


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: int | None = None


class Item(ItemBase):
    id: str

    model_config = ConfigDict(from_attributes=True)
