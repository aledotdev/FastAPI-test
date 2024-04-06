from typing import TYPE_CHECKING

import arrow

from event_provider import models, schemas
from event_provider.logger import logger
from event_provider.services import events as events_services
from event_provider.services.fetch_provider_events import fetch_provider_event_data, parse_provider_event_data

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio.session import AsyncSession


async def sync_provider_events(provider: models.Provider, session: "AsyncSession"):
    raw_base_event_data = parse_provider_event_data(await fetch_provider_event_data(provider.events_api_url))
    for base_event_data in raw_base_event_data:
        async with session.begin():
            try:
                base_event = await _provider_base_event_create_or_update(provider, base_event_data, session)
            except:  # pylint: disable=bare-except
                msg = "Sync error for BaseEvent. Provider: %s data: %s"
                logger.exception(msg, provider.id, base_event_data)
                continue

            for event_data in base_event_data.events:
                try:
                    event = await _provider_event_create_or_update(provider, base_event, event_data, session)
                except:  # pylint: disable=bare-except
                    msg = "Sync error for Event. Provider: %s BaseEvent: %s data: %s"
                    logger.exception(msg, provider.id, base_event.id, event_data)
                    continue

                for zone_data in event_data.zones:
                    try:
                        await _provider_event_zone_create_or_update(provider, event, zone_data, session)
                    except:  # pylint: disable=bare-except
                        msg = "Sync error for EventZone. Provider: %s Event: %s data: %s"
                        logger.exception(msg, provider.id, event.id, zone_data)


async def _provider_base_event_create_or_update(
    provider: models.Provider,
    base_event_data: schemas.FetchProviderBaseEvent,
    session: "AsyncSession",
) -> models.ProviderBaseEvent:

    base_event = await events_services.get_provider_base_event(provider, base_event_data.base_event_id, session)
    if not base_event:
        base_event = await events_services.provider_base_event_create(
            provider,
            schemas.ProviderBaseEventCreate(
                base_event_id=base_event_data.base_event_id,
                sell_mode=base_event_data.sell_mode,
                title=base_event_data.title,
                organizer_company_id=base_event_data.organizer_company_id,
            ),
            session,
        )
    else:
        await events_services.provider_base_event_update(
            base_event,
            schemas.ProviderBaseEventUpdate(sell_mode=base_event_data.sell_mode, title=base_event_data.title),
            session,
        )
    return base_event


async def _provider_event_create_or_update(
    provider: models.Provider,
    base_event: models.ProviderBaseEvent,
    event_data: schemas.FetchProviderEvent,
    session: "AsyncSession",
) -> models.ProviderEvent:
    event = await events_services.get_provider_event(provider, base_event, event_data.event_id, session)
    if not event:
        event = await events_services.provider_event_create(
            provider,
            base_event,
            schemas.ProviderEventCreate(
                event_id=event_data.event_id,
                event_start_date=arrow.get(event_data.event_start_date).datetime,
                event_end_date=arrow.get(event_data.event_end_date).datetime,
                sell_from=arrow.get(event_data.sell_from).datetime,
                sell_to=arrow.get(event_data.sell_to).datetime,
                sold_out=event_data.sold_out,
            ),
            session,
        )
    else:
        await events_services.provider_event_update(
            event,
            schemas.ProviderEventUpdate(
                event_start_date=arrow.get(event_data.event_start_date).datetime,
                event_end_date=arrow.get(event_data.event_end_date).datetime,
                sell_from=arrow.get(event_data.sell_from).datetime,
                sell_to=arrow.get(event_data.sell_to).datetime,
                sold_out=event_data.sold_out,
            ),
            session,
        )
    return event


async def _provider_event_zone_create_or_update(
    provider: models.Provider,
    event: models.ProviderEvent,
    event_zone_data: schemas.FetchProviderEventZone,
    session: "AsyncSession",
) -> models.ProviderEvent:
    zone = await events_services.get_provider_event_zone(provider, event, event_zone_data.zone_id, session)
    if not zone:
        zone = await events_services.provider_event_zone_create(
            provider,
            event,
            schemas.ProviderEventZoneCreate(
                zone_id=event_zone_data.zone_id,
                capacity=event_zone_data.capacity,
                price=event_zone_data.price,
                name=event_zone_data.name,
                numbered=event_zone_data.numbered,
            ),
            session,
        )
    else:
        await events_services.provider_event_zone_update(
            zone,
            schemas.ProviderEventZoneUpdate(
                capacity=event_zone_data.capacity,
                price=event_zone_data.price,
                name=event_zone_data.name,
                numbered=event_zone_data.numbered,
            ),
            session,
        )
    return zone
