from datetime import datetime

from pydantic import BaseModel


class ProviderBase(BaseModel):
    name: str
    events_api_url: str


class ProviderCreate(ProviderBase):
    pass


class ProviderUpdate(ProviderBase):
    pass


class ProviderBaseEventBase(BaseModel):
    sell_mode: str
    title: str


class ProviderBaseEventCreate(ProviderBaseEventBase):
    base_event_id: int
    organizer_company_id: int | None = None


class ProviderBaseEventUpdate(ProviderBaseEventBase):
    pass


class ProviderEventBase(BaseModel):
    event_start_date: datetime
    event_end_date: datetime
    sell_from: datetime
    sell_to: datetime
    sold_out: bool


class ProviderEventCreate(ProviderEventBase):
    event_id: int


class ProviderEventUpdate(ProviderEventBase):
    pass


class ProviderEventZoneBase(BaseModel):
    capacity: int
    price: float
    name: str
    numbered: bool


class ProviderEventZoneCreate(ProviderEventZoneBase):
    zone_id: int


class ProviderEventZoneUpdate(ProviderEventZoneBase):
    pass


class FetchProviderEventZone(BaseModel):
    zone_id: int
    capacity: int
    price: float
    name: str
    numbered: bool


class FetchProviderEvent(BaseModel):
    event_id: int
    event_start_date: str
    event_end_date: str
    sell_from: str
    sell_to: str
    sold_out: bool
    zones: list


class FetchProviderBaseEvent(BaseModel):
    base_event_id: int
    sell_mode: str
    title: str
    organizer_company_id: int | None = None
    events: list[FetchProviderEvent]
