from sqlalchemy.orm import Session

from .. import models, schemas


def get_provider(provider_id: int, db: Session) -> models.Provider | None:
    query = db.query(models.Provider)
    query = query.filter(models.Provider.id == provider_id)
    return query.first()


def provider_create(provider_data: schemas.ProviderCreate, db: Session) -> models.Provider:
    db_provider = models.Provider(name=provider_data.name)
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return db_provider


def provider_update(provider: models.Provider, provider_data: schemas.ProviderUpdate, db: Session) -> models.Provider:
    provider.name = provider_data.name
    db.commit()
    return provider


def get_provider_base_event(
    provider: models.Provider, base_event_id: int, db: Session
) -> models.ProviderBaseEvent | None:
    query = db.query(models.ProviderBaseEvent)
    query = query.filter(models.ProviderBaseEvent.provider_id == provider.id)
    query = query.filter(models.ProviderBaseEvent.base_event_id == base_event_id)
    return query.first()


def provider_base_event_create(
    provider: models.Provider, provider_base_event_data: schemas.ProviderBaseEventCreate, db: Session
) -> models.ProviderBaseEvent:
    db_provider_base_event = models.ProviderBaseEvent(
        provider=provider,
        base_event_id=provider_base_event_data.base_event_id,
        sell_mode=provider_base_event_data.sell_mode,
        title=provider_base_event_data.title,
        organizer_company_id=provider_base_event_data.organizer_company_id,
    )
    db.add(db_provider_base_event)
    db.commit()
    db.refresh(db_provider_base_event)
    return db_provider_base_event


def provider_base_event_update(
    provider_base_event: models.ProviderBaseEvent,
    provider_base_event_data: schemas.ProviderBaseEventUpdate,
    db: Session,
):
    provider_base_event.sell_mode = provider_base_event_data.sell_mode
    provider_base_event.title = provider_base_event_data.title
    db.commit()
    return provider_base_event


def get_provider_event(provider: models.Provider, event_id: int, db: Session):
    query = db.query(models.ProviderEvent)
    query = query.filter(models.ProviderEvent.provider_id == provider.id)
    query = query.filter(models.ProviderEvent.event_id == event_id)
    return query.first()


def provider_event_create(
    provider: models.Provider,
    provider_base_event: models.ProviderBaseEvent,
    provider_event_data: schemas.ProviderEventCreate,
    db: Session,
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
    db.add(db_provider_event)
    db.commit()
    db.refresh(db_provider_event)
    return db_provider_event


def provider_event_update(
    provider_event: models.ProviderEvent,
    provider_event_data: schemas.ProviderEventUpdate,
    db: Session,
):
    provider_event.event_start_date = provider_event_data.event_start_date
    provider_event.event_start_time = provider_event_data.event_start_date.time()
    provider_event.event_end_date = provider_event_data.event_end_date
    provider_event.event_end_time = provider_event_data.event_end_date.time()
    provider_event.sell_from = provider_event_data.sell_from
    provider_event.sell_to = provider_event_data.sell_to
    provider_event.sold_out = provider_event_data.sold_out

    db.commit()
    return provider_event


def provider_event_zone_add(
    provider_event: models.ProviderBaseEvent,
    provider_event_data: schemas.ProviderEventZoneAdd,
    db: Session,
) -> models.ProviderEventZone:
    db_provider_event_zone = models.ProviderEventZone(
        provider=provider_event.provider,
        provider_event=provider_event,
        zone_id=provider_event_data.zone_id,
        capacity=provider_event_data.capacity,
        price=provider_event_data.price,
        name=provider_event_data.name,
        numbered=provider_event_data.numbered,
    )
    db.add(db_provider_event_zone)
    db.commit()
    db.refresh(db_provider_event_zone)
    return db_provider_event_zone
