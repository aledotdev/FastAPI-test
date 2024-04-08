import asyncio

import click

from event_provider import models  # pylint: disable=unused-import
from event_provider.database import get_database_engine, init_db
from event_provider.settings import get_settings


async def _run(dropall):
    engine = get_database_engine(get_settings())
    await init_db(engine, dropall=dropall)


@click.command("Create new Database and Tables")
@click.option("--dropall", is_flag=True, show_default=True, default=False, help="Drop existing database tales")
def main(dropall=False):
    asyncio.run(_run(dropall))


if __name__ == "__main__":
    main()
