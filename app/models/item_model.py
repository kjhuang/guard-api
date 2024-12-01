"""
ite model
"""

from sqlalchemy import Column, Integer, String

from app.db.database import Base


class Item(Base):
    """
    item model
    """

    __tablename__ = "item"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Integer)
