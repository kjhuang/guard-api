"""
site model
"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Site(Base):
    """
    Site model
    """

    __tablename__ = "site"

    site_id = Column(String(64), primary_key=True)
    site_name = Column(String(60), nullable=False)

    # Relationship with Announce
    announcements = relationship("Announce", back_populates="site")

    # Relationship with repair order
    repair_orders = relationship("RepairOrder", back_populates="site")
