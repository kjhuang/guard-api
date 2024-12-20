"""
payment_order model
"""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class PaymentOrder(Base):
    __tablename__ = "payment_order"

    id = Column(String(64), primary_key=True, nullable=False)
    site_id = Column(String(64), ForeignKey("site.site_id"), nullable=False)
    building_id = Column(String(64), ForeignKey("building.building_id"), nullable=False)
    house_no = Column(String(60), nullable=False)
    house_owner = Column(String(60), nullable=False)
    payment_item = Column(String(60), nullable=False)
    amount = Column(Integer, nullable=False)
    payment_due_date = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime)
    created_by = Column(String(64))

    # relationship to site
    site = relationship("Site")

    # relationship to building
    building = relationship("Building", back_populates="payment_orders")
