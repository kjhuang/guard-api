"""
database async
"""

import os

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import AsyncAdaptedQueuePool

ASYNC_DB_URI = "postgresql+asyncpg://{user}:{pw}@{host}:{port}/{db}"

ASYNC_POSTGRES = {
    "user": os.getenv("DB_USERNAME", ""),
    "pw": os.getenv("DB_PWD", ""),
    "db": os.getenv("DB_NAME", ""),
    "host": os.getenv("DB_HOST", ""),
    "port": os.getenv("DB_PORT", ""),
}

print(ASYNC_POSTGRES)

async_engine: AsyncEngine = create_async_engine(
    ASYNC_DB_URI.format(**ASYNC_POSTGRES),
    poolclass=AsyncAdaptedQueuePool,
    pool_size=30,
    max_overflow=10,
    pool_pre_ping=True,
    echo=False,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
)

Base = declarative_base()  # inherit from this class to create ORM models


async def get_async_db_session():
    # session: AsyncSession = AsyncSessionLocal()
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
