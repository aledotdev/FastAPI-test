import asyncio
from typing import TYPE_CHECKING

from event_provider.logger import logger
from event_provider.services.sync_provider_events import sync_provider_events

if TYPE_CHECKING:
    from event_provider.database import DBSessionType
    from event_provider.models import Provider


async def run_provider_event_sync(provider: "Provider", wait_time: int, db_session: "DBSessionType"):
    while True:
        async with db_session() as session:
            logger.info("Running sync for provider [%s] %s", provider.id, provider.name)
            await sync_provider_events(provider, session)

        await asyncio.sleep(wait_time)
