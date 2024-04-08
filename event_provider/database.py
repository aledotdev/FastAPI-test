from typing import TypeAlias

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from event_provider.settings import Settings, get_settings

DBBase = declarative_base()
DBSessionType: TypeAlias = async_sessionmaker[AsyncSession]


def get_database_engine(settings: Settings) -> AsyncEngine:
    if not settings.DB_ENGINE:
        settings.DB_ENGINE = create_async_engine(settings.DB_URL, connect_args={})
    return settings.DB_ENGINE


def get_db_session(settings: Settings | None = None) -> DBSessionType:
    if not settings:
        settings = get_settings()
    engine = get_database_engine(settings)
    return async_sessionmaker(engine, expire_on_commit=False)


async def init_db(engine: AsyncEngine, dropall: bool = False):
    if dropall:
        async with engine.begin() as conn:
            await conn.run_sync(DBBase.metadata.drop_all)

    async with engine.begin() as conn:
        await conn.run_sync(DBBase.metadata.create_all)
