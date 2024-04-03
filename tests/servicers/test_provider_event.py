import arrow

from event_provider import schemas
from event_provider.services import events as events_services


def test_create_provider_event(test_provider, test_provider_base_event, db):
    start = arrow.get("2024-04-10T20:00:00+00")
    end = arrow.get("2024-04-10T21:00:00")
    provider_event = events_services.provider_event_create(
        test_provider,
        test_provider_base_event,
        schemas.ProviderEventCreate(
            event_id=555,
            event_start_date=start.datetime,
            event_end_date=end.datetime,
            sell_from=start.shift(days=-3).datetime,
            sell_to=start.shift(seconds=-5).datetime,
            sold_out=False,
        ),
        db,
    )

    assert provider_event.provider == test_provider
    assert provider_event.provider_base_event == test_provider_base_event
    assert provider_event.event_id == 555
    assert provider_event.event_start_date == start.datetime
    assert provider_event.event_start_time == start.datetime.time()
    assert provider_event.event_end_date == end.datetime
    assert provider_event.event_end_time == end.datetime.time()
    assert provider_event.sell_from == start.shift(days=-3).datetime
    assert provider_event.sell_to == start.shift(seconds=-5).datetime
    assert provider_event.sold_out is False


def test_update_provider_event(test_provider, test_provider_event, db):
    new_start = arrow.get("2024-10-10T22:00:00+00")
    new_end = arrow.get("2024-10-10T23:00:00")
    events_services.provider_event_update(
        test_provider_event,
        schemas.ProviderEventUpdate(
            event_start_date=new_start.datetime,
            event_end_date=new_end.datetime,
            sell_from=new_start.shift(days=-1).datetime,
            sell_to=new_start.shift(seconds=-1).datetime,
            sold_out=True,
        ),
        db,
    )

    updated_provider_event = events_services.get_provider_event(test_provider, test_provider_event.event_id, db)

    assert updated_provider_event.id == test_provider_event.id
    assert updated_provider_event.event_start_date == new_start.datetime
    assert updated_provider_event.event_end_date == new_end.datetime
    assert updated_provider_event.sell_from == new_start.shift(days=-1).datetime
    assert updated_provider_event.sell_to == new_start.shift(seconds=-1).datetime
    assert updated_provider_event.sold_out is True


def test_get_provider_event(test_provider, test_provider_event, db):
    provider_event = events_services.get_provider_event(test_provider, test_provider_event.event_id, db)

    assert provider_event.id == test_provider_event.id
    assert provider_event.event_id == test_provider_event.event_id


def test_provider_zone_add(test_provider_event, db):
    provider_zone = events_services.provider_event_zone_add(
        test_provider_event,
        schemas.ProviderEventZoneAdd(
            zone_id=111,
            capacity=333,
            price=35.99,
            name="Test Zone",
            numbered=True,
        ),
        db,
    )

    assert provider_zone.zone_id == 111
    assert provider_zone.capacity == 333
    assert provider_zone.price == 35.99
    assert provider_zone.name == "Test Zone"
    assert provider_zone.numbered is True
