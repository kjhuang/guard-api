"""
repair_order model
"""

from sqlalchemy import Column, DateTime, String

from app.db.database import Base


class RepairOrder(Base):
    __tablename__ = "repair_order"

    id = Column(String(64), primary_key=True, nullable=False)
    applicant = Column(String(20), nullable=False)
    region = Column(String(20), nullable=False)
    item_type = Column(String(20), nullable=False)
    description = Column(String(200), nullable=True)
    designated_service = Column(String(20), nullable=True)
    reservation_by = Column(String(20), nullable=True)
    appointment_time = Column(String(30), nullable=True)
    created_at = Column(DateTime, nullable=True)
    created_by = Column(String(64), nullable=True)
