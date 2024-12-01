"""
database config
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URI = "postgresql://{user}:{pw}@{host}:{port}/{db}"

POSTGRES = {
    "user": os.getenv("DB_USERNAME", ""),
    "pw": os.getenv("DB_PWD", ""),
    "db": os.getenv("DB_NAME", ""),
    "host": os.getenv("DB_HOST", ""),
    "port": os.getenv("DB_PORT", ""),
}

print(POSTGRES)

engine = create_engine(DB_URI.format(**POSTGRES), echo=False)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()  # inherit from this class to create ORM models


def get_db_session():
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
