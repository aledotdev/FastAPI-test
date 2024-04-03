from datetime import datetime
from pydantic import BaseModel


class ProviderCreate(BaseModel):
    name: str


class ProviderUpdate(BaseModel):
    name: str


class ProviderBaseEventCreate(BaseModel):
    base_event_id: int
    sell_mode: str
    title: str
    organizer_company_id: int


class ProviderBaseEventUpdate(BaseModel):
    sell_mode: str
    title: str


class ProviderEventCreate(BaseModel):
    event_id: int
    event_start_date: datetime
    event_end_date: datetime
    sell_from: datetime
    sell_to: datetime
    sold_out: bool


class ProviderEventUpdate(BaseModel):
    event_start_date: datetime
    event_end_date: datetime
    sell_from: datetime
    sell_to: datetime
    sold_out: bool


class ProviderEventZoneAdd(BaseModel):
    zone_id: int
    capacity: int
    price: float
    name: str
    numbered: bool
