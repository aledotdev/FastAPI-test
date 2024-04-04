from event_provider import schemas
from event_provider.services import events as events_services


def test_create_provider(db):
    provider_1 = events_services.provider_create(
        schemas.ProviderCreate(name="New Provider", events_api_url="https://example.com"), db
    )
    provider_2 = events_services.provider_create(
        schemas.ProviderCreate(name="Other Provider", events_api_url="https://test.com"), db
    )

    assert provider_1.id != provider_2.id
    assert provider_1.name == "New Provider"
    assert provider_1.events_api_url == "https://example.com"
    assert provider_2.name == "Other Provider"
    assert provider_2.events_api_url == "https://test.com"


def test_get_provider(db):
    providers_ids = []
    for i in range(3):
        provider = events_services.provider_create(
            schemas.ProviderCreate(name=f"Provider {i}", events_api_url=f"https://test{1}.com"), db
        )
        providers_ids.append(provider.id)

    for i, provider_id in enumerate(providers_ids):
        provider = events_services.get_provider(provider_id, db)
        assert provider is not None
        assert provider.id == provider_id
        assert provider.name == f"Provider {i}"


def test_provider_update(test_provider, db):
    events_services.provider_update(
        test_provider, schemas.ProviderUpdate(name="Provider Updated", events_api_url="https://test.com"), db
    )
    updated_provider = events_services.get_provider(test_provider.id, db)
    assert updated_provider.id == test_provider.id
    assert updated_provider.name == test_provider.name
    assert updated_provider.name == "Provider Updated"
    assert updated_provider.events_api_url == "https://test.com"
