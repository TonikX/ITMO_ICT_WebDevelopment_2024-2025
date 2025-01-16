from sqlalchemy import make_url
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine, AsyncEngine

from app.config.models import DatabaseConfig


def create_engine(config: DatabaseConfig) -> AsyncEngine:
    return create_async_engine(url=make_url(config.uri))


def create_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    pool: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine, expire_on_commit=False, autoflush=False
    )
    return pool
