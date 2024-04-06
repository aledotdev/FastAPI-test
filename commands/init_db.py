import asyncio

import click

from event_provider import models  # pylint: disable=unused-import
from event_provider.database import get_database_engine, init_db
from event_provider.settings import get_settings


async def _run():
    engine = get_database_engine(get_settings())
    await init_db(engine, dropall=True)


@click.command("Start event sync service for all providers")
def main():
    asyncio.run(_run())


if __name__ == "__main__":
    main()
