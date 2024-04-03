from event_provider import schemas
from event_provider.services import events as events_services


def test_create_provider_base_event(test_provider, db):
    provider_base_event_1 = events_services.provider_base_event_create(
        test_provider,
        schemas.ProviderBaseEventCreate(
            base_event_id=100, sell_mode="offline", title="Base Event 1", organizer_company_id=111
        ),
        db,
    )
    provider_base_event_2 = events_services.provider_base_event_create(
        test_provider,
        schemas.ProviderBaseEventCreate(
            base_event_id=200, sell_mode="online", title="Base Event 2", organizer_company_id=222
        ),
        db,
    )

    assert provider_base_event_1.provider == test_provider
    assert provider_base_event_1.base_event_id == 100
    assert provider_base_event_1.sell_mode.name == "offline"
    assert provider_base_event_1.title == "Base Event 1"
    assert provider_base_event_1.organizer_company_id == 111

    assert provider_base_event_2.provider == test_provider
    assert provider_base_event_2.base_event_id == 200
    assert provider_base_event_2.sell_mode.name == "online"
    assert provider_base_event_2.title == "Base Event 2"
    assert provider_base_event_2.organizer_company_id == 222


def test_get_provider_base_event(test_provider, db):
    base_event_ids = []
    for i in range(1, 3):
        provider_base_event = events_services.provider_base_event_create(
            test_provider,
            schemas.ProviderBaseEventCreate(
                base_event_id=i * 100, sell_mode="online", title=f"Base Event {i}", organizer_company_id=i * 10
            ),
            db,
        )
        base_event_ids.append(provider_base_event.id)

    for i, _id in enumerate(base_event_ids, start=1):
        base_event_id = i * 100
        provider_base_event = events_services.get_provider_base_event(test_provider, base_event_id, db)

        assert provider_base_event is not None
        assert provider_base_event.id == _id
        assert provider_base_event.provider == test_provider
        assert provider_base_event.base_event_id == base_event_id
        assert provider_base_event.sell_mode.name == "online"
        assert provider_base_event.title == f"Base Event {i}"
        assert provider_base_event.organizer_company_id == i * 10


def test_update_provider_base_event(test_provider, test_provider_base_event, db):
    events_services.provider_base_event_update(
        test_provider_base_event, schemas.ProviderBaseEventUpdate(sell_mode="offline", title="Base Event updated"), db
    )
    updated_provider_base_event = events_services.get_provider_base_event(test_provider, 100, db)

    assert test_provider_base_event.id == updated_provider_base_event.id
    assert test_provider_base_event.provider == updated_provider_base_event.provider
    assert test_provider_base_event.base_event_id == updated_provider_base_event.base_event_id
    assert test_provider_base_event.title == updated_provider_base_event.title
    assert test_provider_base_event.sell_mode == updated_provider_base_event.sell_mode
