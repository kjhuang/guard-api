"""
announce model
"""

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Announce(Base):
    __tablename__ = "announce"

    id = Column(String(64), primary_key=True)
    site_id = Column(String(64), ForeignKey("site.site_id"), nullable=False)
    title = Column(String(100), nullable=False)
    severity = Column(String(20))
    content_path = Column(String(600))
    publish_date = Column(DateTime)

    # Relationship with Site
    site = relationship("Site", back_populates="announcements")
