"""
common schema
"""

from pydantic import BaseModel


class LookupValue(BaseModel):
    id: str
    value: str
