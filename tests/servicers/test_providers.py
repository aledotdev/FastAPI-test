import pytest

from event_provider import schemas
from event_provider.services import events as events_services


@pytest.mark.asyncio
async def test_create_provider(async_session):
    async with async_session() as session:
        async with session.begin():
            provider_1 = await events_services.provider_create(
                schemas.ProviderCreate(name="New Provider", events_api_url="https://example.com"), session
            )
            provider_2 = await events_services.provider_create(
                schemas.ProviderCreate(name="Other Provider", events_api_url="https://test.com"), session
            )

    async with async_session() as session:
        new_provider_1 = await events_services.get_provider(provider_1.id, session)
        new_provider_2 = await events_services.get_provider(provider_2.id, session)
        assert new_provider_1.id != new_provider_2.id
        assert new_provider_1.name == "New Provider"
        assert new_provider_1.events_api_url == "https://example.com"
        assert new_provider_2.name == "Other Provider"
        assert new_provider_2.events_api_url == "https://test.com"


@pytest.mark.asyncio
async def test_get_provider(async_session):
    providers = []
    async with async_session() as session:
        async with session.begin():
            for i in range(3):
                providers.append(
                    await events_services.provider_create(
                        schemas.ProviderCreate(name=f"Provider {i}", events_api_url=f"https://test{i}.com"), session
                    )
                )

    async with async_session() as session:
        for i, provider in enumerate(providers):
            new_provider = await events_services.get_provider(provider.id, session)
            assert new_provider is not None
            assert new_provider.id == provider.id
            assert new_provider.name == f"Provider {i}"
            assert new_provider.events_api_url == f"https://test{i}.com"


@pytest.mark.asyncio
async def test_provider_update(test_provider, async_session):
    async with async_session() as session:
        async with session.begin():
            await events_services.provider_update(
                test_provider,
                schemas.ProviderUpdate(name="Provider Updated", events_api_url="https://test.com"),
                session,
            )
    async with async_session() as session:
        updated_provider = await events_services.get_provider(test_provider.id, session)
        assert updated_provider.id == test_provider.id
        assert updated_provider.name == test_provider.name
        assert updated_provider.name == "Provider Updated"
        assert updated_provider.events_api_url == "https://test.com"
