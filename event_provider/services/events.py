from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from .. import models, schemas

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio.session import AsyncSession


async def get_provider(provider_id: int, db_session: "AsyncSession") -> models.Provider | None:
    return await db_session.get(models.Provider, provider_id)


async def provider_create(provider_data: schemas.ProviderCreate, db_session: "AsyncSession") -> models.Provider:
    db_provider = models.Provider(name=provider_data.name, events_api_url=provider_data.events_api_url)
    db_session.add(db_provider)
    return db_provider


async def provider_update(
    provider: models.Provider, provider_data: schemas.ProviderUpdate, db_session: "AsyncSession"
) -> models.Provider:
    provider.name = provider_data.name
    provider.events_api_url = provider_data.events_api_url
    db_session.add(provider)
    return provider


async def get_provider_base_event(
    provider: models.Provider, base_event_id: int, db_session: "AsyncSession", load_events: bool = False
) -> models.ProviderBaseEvent | None:
    query = (
        select(models.ProviderBaseEvent)
        .where(models.ProviderBaseEvent.provider_id == provider.id)
        .where(models.ProviderBaseEvent.base_event_id == base_event_id)
    )
    if load_events:
        query = query.options(joinedload(models.ProviderBaseEvent.events).subqueryload(models.ProviderEvent.zones))
    return await db_session.scalar(query)


async def provider_base_event_create(
    provider: models.Provider, provider_base_event_data: schemas.ProviderBaseEventCreate, db_session: "AsyncSession"
) -> models.ProviderBaseEvent:
    db_provider_base_event = models.ProviderBaseEvent(
        provider=provider,
        base_event_id=provider_base_event_data.base_event_id,
        sell_mode=getattr(models.SellModeEnum, provider_base_event_data.sell_mode),
        title=provider_base_event_data.title,
        organizer_company_id=provider_base_event_data.organizer_company_id,
    )
    db_session.add(db_provider_base_event)
    return db_provider_base_event


async def provider_base_event_update(
    provider_base_event: models.ProviderBaseEvent,
    provider_base_event_data: schemas.ProviderBaseEventUpdate,
    db_session: "AsyncSession",
):
    provider_base_event.sell_mode = provider_base_event_data.sell_mode
    provider_base_event.title = provider_base_event_data.title
    db_session.add(provider_base_event)
    return provider_base_event


async def get_provider_event(provider: models.Provider, event_id: int, db_session: "AsyncSession"):
    query = (
        select(models.ProviderEvent)
        .filter(models.ProviderEvent.provider_id == provider.id)
        .filter(models.ProviderEvent.event_id == event_id)
    )
    return await db_session.scalar(query)


async def provider_event_create(
    provider: models.Provider,
    provider_base_event: models.ProviderBaseEvent,
    provider_event_data: schemas.ProviderEventCreate,
    db_session: "AsyncSession",
) -> models.ProviderEvent:
    db_provider_event = models.ProviderEvent(
        provider=provider,
        provider_base_event_id=provider_base_event.id,
        event_id=provider_event_data.event_id,
        event_start_date=provider_event_data.event_start_date,
        event_start_time=provider_event_data.event_start_date.time(),
        event_end_date=provider_event_data.event_end_date,
        event_end_time=provider_event_data.event_end_date.time(),
        sell_from=provider_event_data.sell_from,
        sell_to=provider_event_data.sell_to,
        sold_out=provider_event_data.sold_out,
    )
    db_session.add(db_provider_event)
    return db_provider_event


async def provider_event_update(
    provider_event: models.ProviderEvent,
    provider_event_data: schemas.ProviderEventUpdate,
    db_session: "AsyncSession",
):
    provider_event.event_start_date = provider_event_data.event_start_date
    provider_event.event_start_time = provider_event_data.event_start_date.time()
    provider_event.event_end_date = provider_event_data.event_end_date
    provider_event.event_end_time = provider_event_data.event_end_date.time()
    provider_event.sell_from = provider_event_data.sell_from
    provider_event.sell_to = provider_event_data.sell_to
    provider_event.sold_out = provider_event_data.sold_out
    db_session.add(provider_event)
    return provider_event


async def provider_event_zone_create(
    provider: models.Provider,
    provider_event: models.ProviderBaseEvent,
    provider_event_zone_data: schemas.ProviderEventZoneCreate,
    db_session: "AsyncSession",
) -> models.ProviderEventZone:
    db_provider_event_zone = models.ProviderEventZone(
        provider=provider,
        provider_event=provider_event,
        zone_id=provider_event_zone_data.zone_id,
        capacity=provider_event_zone_data.capacity,
        price=provider_event_zone_data.price,
        name=provider_event_zone_data.name,
        numbered=provider_event_zone_data.numbered,
    )
    db_session.add(db_provider_event_zone)
    return db_provider_event_zone


async def provider_event_zone_update(
    provider_event_zone: models.ProviderEventZone,
    provider_event_zone_data: schemas.ProviderEventZoneUpdate,
    db_session: "AsyncSession",
) -> models.ProviderEventZone:
    provider_event_zone.capacity = provider_event_zone_data.capacity
    provider_event_zone.price = provider_event_zone_data.price
    provider_event_zone.name = provider_event_zone_data.name
    provider_event_zone.numbered = provider_event_zone_data.numbered
    db_session.add(provider_event_zone)
    return provider_event_zone


async def get_provider_event_zone(
    provider: models.Provider, event: models.ProviderEvent, zone_id: int, db_session: "AsyncSession"
):
    query = (
        select(models.ProviderEventZone)
        .filter(models.ProviderEventZone.provider_id == provider.id)
        .filter(models.ProviderEventZone.provider_event_id == event.id)
        .filter(models.ProviderEventZone.zone_id == zone_id)
    )
    return await db_session.scalar(query)
