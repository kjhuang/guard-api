"""
site model
"""

from sqlalchemy import Column, String

from app.db.database import Base


class Site(Base):
    """
    Site model
    """

    __tablename__ = "site"

    site_id = Column(String, primary_key=True)
    site_name = Column(String)
