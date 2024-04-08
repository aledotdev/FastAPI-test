from datetime import datetime

import arrow
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from event_provider.api.common import BaseObjectListResponse
from event_provider.dependencies import get_api_db_session
from event_provider.services import events as events_services

router = APIRouter()


def _format_event_date(date: datetime) -> str:
    return date.strftime("%Y-%m-%d")


def _format_event_time(date: datetime) -> str:
    return date.strftime("%H:%M:%S")


class EventResponse(BaseModel):
    id: int
    title: str
    start_date: str
    start_time: str
    end_date: str
    end_time: str
    min_price: float
    max_price: float


@router.get("/search/", response_model=BaseObjectListResponse[EventResponse])
async def events_list(
    starts_at: str | None = None, ends_at: str | None = None, offline: bool = False, session=Depends(get_api_db_session)
):
    event_data_list = []

    try:
        _starts_at = arrow.get(starts_at).datetime if starts_at else None
    except (arrow.ParserError, ValueError) as _e:
        raise HTTPException(status_code=400, detail=f"Invalid starts_at date format. date: {starts_at}") from _e

    try:
        _ends_at = arrow.get(ends_at).datetime if ends_at else None
    except arrow.ParserError as _e:
        raise HTTPException(status_code=400, detail=f"Invalid _ends_at date format. date {ends_at}") from _e

    events = await events_services.get_all_events(session, starts_at=_starts_at, ends_at=_ends_at, show_offline=offline)
    for event in events:
        event_data_list.append(
            EventResponse(
                id=event.id,
                title=event.provider_base_event.title,
                start_date=_format_event_date(event.event_start_date),
                start_time=_format_event_time(event.event_start_date),
                end_date=_format_event_date(event.event_end_date),
                end_time=_format_event_time(event.event_end_date),
                min_price=event.min_price,
                max_price=event.max_price,
            )
        )

    return {"data": event_data_list}
