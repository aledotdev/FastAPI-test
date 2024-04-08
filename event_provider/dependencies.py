from event_provider.database import get_db_session


async def get_api_db_session():  # -> AsyncSession:
    async with get_db_session()() as session:
        yield session
