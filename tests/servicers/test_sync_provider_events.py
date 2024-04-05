from unittest import mock

import arrow
import pytest

from event_provider.services import events as events_services
from event_provider.services import sync_provider_events


@pytest.mark.asyncio
@mock.patch("event_provider.services.sync_provider_events.fetch_provider_event_data")
async def test_provider_events_sync_fetch(
    fetch_provider_event_data_mock, test_provider, provider_events_xml_example, async_session
):
    async with async_session() as session:
        fetch_provider_event_data_mock.return_value = provider_events_xml_example
        await sync_provider_events.sync_provider_events(test_provider, session)

        base_event = await events_services.get_provider_base_event(test_provider, 291, session)
        event = await events_services.get_provider_event(test_provider, 291, session)
        zone = await events_services.get_provider_event_zone(test_provider, event, 40, session)

    assert base_event is not None
    assert base_event.sell_mode.name == "online"
    assert base_event.title == "Camela en concierto"

    assert event.provider_id == test_provider.id
    assert event.provider_base_event_id == base_event.id
    assert event.event_id == 291
    assert event.event_start_date == arrow.get("2021-06-30T21:00:00").datetime
    assert event.event_start_time == arrow.get("2021-06-30T21:00:00").datetime.time()
    assert event.event_end_date == arrow.get("2021-06-30T22:00:00").datetime
    assert event.event_end_time == arrow.get("2021-06-30T22:00:00").datetime.time()
    assert event.sell_from == arrow.get("2020-07-01T00:00:00").datetime
    assert event.sell_to == arrow.get("2021-06-30T20:00:00").datetime
    assert event.sold_out is False

    assert zone.provider_id == test_provider.id
    assert zone.provider_event_id == event.id
    assert zone.zone_id == 40
    assert zone.capacity == 243
    assert zone.price == 20.0
    assert zone.name == "Platea"
    assert zone.numbered is True
