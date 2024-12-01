"""
order model
"""

from sqlalchemy import Column, Integer, String

from app.db.database import Base


class Order(Base):
    __tablename__ = "order"

    user_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False)
