import pytest

from event_provider import schemas
from event_provider.services import events as events_services


@pytest.mark.asyncio
async def test_create_provider_base_event(test_provider, async_session):
    async with async_session() as session:
        async with session.begin():
            provider_base_event_1 = await events_services.provider_base_event_create(
                test_provider,
                schemas.ProviderBaseEventCreate(
                    base_event_id=100, sell_mode="offline", title="Base Event 1", organizer_company_id=111
                ),
                session,
            )
            provider_base_event_2 = await events_services.provider_base_event_create(
                test_provider,
                schemas.ProviderBaseEventCreate(
                    base_event_id=200, sell_mode="online", title="Base Event 2", organizer_company_id=222
                ),
                session,
            )

        assert provider_base_event_1.provider_id == test_provider.id
        assert provider_base_event_1.base_event_id == 100
        assert provider_base_event_1.sell_mode.name == "offline"
        assert provider_base_event_1.title == "Base Event 1"
        assert provider_base_event_1.organizer_company_id == 111

        assert provider_base_event_2.provider_id == test_provider.id
        assert provider_base_event_2.base_event_id == 200
        assert provider_base_event_2.sell_mode.name == "online"
        assert provider_base_event_2.title == "Base Event 2"
        assert provider_base_event_2.organizer_company_id == 222


@pytest.mark.asyncio
async def test_get_provider_base_event(test_provider, async_session):
    base_events = []
    async with async_session() as session:
        async with session.begin():
            for i in range(1, 3):
                provider_base_event = await events_services.provider_base_event_create(
                    test_provider,
                    schemas.ProviderBaseEventCreate(
                        base_event_id=i * 100, sell_mode="online", title=f"Base Event {i}", organizer_company_id=i * 10
                    ),
                    session,
                )
                base_events.append(provider_base_event)

    async with async_session() as session:
        for i, provider_base_event in enumerate(base_events, start=1):
            base_event_id = i * 100
            updated_provider_base_event = await events_services.get_provider_base_event(
                test_provider, base_event_id, session
            )
            assert updated_provider_base_event is not None
            assert updated_provider_base_event.id == provider_base_event.id
            assert updated_provider_base_event.provider_id == test_provider.id
            assert updated_provider_base_event.base_event_id == base_event_id
            assert updated_provider_base_event.sell_mode.name == "online"
            assert updated_provider_base_event.title == f"Base Event {i}"
            assert updated_provider_base_event.organizer_company_id == i * 10


@pytest.mark.asyncio
async def test_update_provider_base_event(test_provider, test_provider_base_event, async_session):
    async with async_session() as session:
        async with session.begin():
            await events_services.provider_base_event_update(
                test_provider_base_event,
                schemas.ProviderBaseEventUpdate(sell_mode="offline", title="Base Event updated"),
                session,
            )
        updated_provider_base_event = await events_services.get_provider_base_event(test_provider, 100, session)

    assert test_provider_base_event.id == updated_provider_base_event.id
    assert test_provider_base_event.provider_id == updated_provider_base_event.provider.id
    assert test_provider_base_event.base_event_id == updated_provider_base_event.base_event_id
    assert test_provider_base_event.title == updated_provider_base_event.title
    assert test_provider_base_event.sell_mode == updated_provider_base_event.sell_mode
