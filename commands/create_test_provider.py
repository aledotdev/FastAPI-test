import asyncio

import click

from event_provider import schemas
from event_provider.database import get_db_session
from event_provider.services import events as events_services


async def _run():
    db_session = get_db_session()
    async with db_session() as session:
        async with session.begin():
            await events_services.provider_create(
                schemas.ProviderCreate(
                    name="Test Provider",
                    events_api_url="https://----",
                ),
                session,
            )

        for provider in await events_services.get_all_providers(session):
            print(f"New Provider: [{provider.id}] {provider.name}")


@click.command("Create a Provider for testing")
def main():
    asyncio.run(_run())


if __name__ == "__main__":
    main()
