from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from core.config import postgres_config

SQLALCHEMY_DATABASE_URL = postgres_config.DATABASE_URL
Base = declarative_base()

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,
)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def async_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
