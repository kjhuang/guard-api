"""
order schema
"""

from pydantic import BaseModel, ConfigDict


class Order(BaseModel):
    user_id: int
    order_id: int
    status: str

    model_config = ConfigDict(from_attributes=True)
