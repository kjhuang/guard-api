"""
building model
"""

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Building(Base):
    """
    Building model
    """

    __tablename__ = "building"
    site_id = Column(String(64), ForeignKey("site.site_id"), primary_key=True)
    building_id = Column(String(64), primary_key=True)
    building_name = Column(String(60), nullable=False)

    # Relationship with Site
    site = relationship("Site", back_populates="buildings")
