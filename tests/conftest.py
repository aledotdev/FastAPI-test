import arrow
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker

from event_provider import database, schemas
from event_provider.services import events as events_services
from event_provider.settings import get_settings


def pytest_configure():
    get_settings(env="test", reload=True)


@pytest.fixture(name="test_settings", scope="session")
def fixtute_test_settings():
    yield get_settings(env="test")


@pytest.fixture(name="db_engine")
def fixture_db_engine(test_settings):
    yield database.create_async_engine(test_settings.TEST_DB_URL)


@pytest_asyncio.fixture(name="async_session")
async def fixture_async_db(db_engine):
    await database.init_db(db_engine, dropall=True)
    async_session = async_sessionmaker(db_engine, expire_on_commit=False)
    yield async_session


@pytest_asyncio.fixture(name="test_provider")
async def fixture_test_provider(async_session):
    async with async_session() as session:
        async with session.begin():
            provider = await events_services.provider_create(
                schemas.ProviderCreate(name="Test Provider", events_api_url="https://example.com"), session
            )
    yield provider


@pytest_asyncio.fixture(name="test_provider_base_event")
async def fixture_test_provider_base_event(test_provider, async_session):
    async with async_session() as session:
        async with session.begin():
            provider_base_event = await events_services.provider_base_event_create(
                test_provider,
                schemas.ProviderBaseEventCreate(
                    base_event_id=100, sell_mode="online", title="Base Event", organizer_company_id=10
                ),
                session,
            )
    yield provider_base_event


@pytest_asyncio.fixture(name="test_provider_event")
async def fixture_test_provider_event(test_provider, test_provider_base_event, async_session):
    start = arrow.get("2024-04-10T20:00:00")
    end = arrow.get("2024-04-10T21:00:00")
    async with async_session() as session:
        async with session.begin():
            provider_event = await events_services.provider_event_create(
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
                session,
            )
    yield provider_event


@pytest.fixture
def provider_events_xml_example():
    with open("tests/utils/provider_events_example.xml", "rb") as fd:
        data = fd.read()
    return data


@pytest.fixture(name="skip_if_sqlite")
def fixture_skip_if_sqlite(db_engine):
    if db_engine.driver in ["sqlite", "aiosqlite"]:
        pytest.skip(reason="Test not compatible with SQLite")
