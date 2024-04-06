import asyncio

import click

from event_provider.database import get_db_session
from event_provider.logger import logger
from event_provider.services.events import get_all_providers
from event_provider.settings import get_settings
from event_provider.tasks import run_provider_event_sync


async def _run():
    logger.info("*** Start provider sync service for all providers ***\n")
    settings = get_settings()
    db_session = get_db_session(settings)

    async with db_session() as session:
        providers = await get_all_providers(session)

    tasks = [
        run_provider_event_sync(provider, settings.EVENTS_SYNC_DELAY_SECONDS, db_session) for provider in providers
    ]
    await asyncio.gather(*tasks)


@click.command("Start event sync service for all providers")
def main():
    asyncio.run(_run())


if __name__ == "__main__":
    main()
