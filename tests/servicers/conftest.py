import arrow
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from event_provider import schemas
from event_provider.database import DBBase
from event_provider.services import events as events_services


@pytest.fixture
def _db():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    DBBase.metadata.create_all(bind=engine)

    with Session(engine) as session:
        yield session

    session.close()


@pytest.fixture(name="db")
def fixture_db():
    url = "postgresql+psycopg2://event_provider:event_provider@localhost:5432/event_provider"
    engine = create_engine(url)
    DBBase.metadata.create_all(bind=engine)

    with Session(engine) as session:
        yield session

    DBBase.metadata.drop_all(bind=engine)
    session.close()


@pytest.fixture(name="test_provider")
def fixture_test_provider(db):
    return events_services.provider_create(
        schemas.ProviderCreate(name="Test Provider", events_api_url="https://example.com"), db
    )


@pytest.fixture(name="test_provider_base_event")
def fixture_test_provider_base_event(test_provider, db):
    return events_services.provider_base_event_create(
        test_provider,
        schemas.ProviderBaseEventCreate(
            base_event_id=100, sell_mode="online", title="Base Event", organizer_company_id=10
        ),
        db,
    )


@pytest.fixture(name="test_provider_event")
def fixture_test_provider_event(test_provider, test_provider_base_event, db):
    start = arrow.get("2024-04-10T20:00:00")
    end = arrow.get("2024-04-10T21:00:00")
    return events_services.provider_event_create(
        test_provider,
        test_provider_base_event,
        schemas.ProviderEventCreate(
            event_id=500,
            event_start_date=start.datetime,
            event_end_date=end.datetime,
            sell_from=start.shift(days=-1).datetime,
            sell_to=start.shift(seconds=-1).datetime,
            sold_out=False,
        ),
        db,
    )
