# pylint: disable=c-extension-no-member

import httpx
from lxml import etree

from event_provider import schemas


def _parse_base_event(node: etree._Element) -> schemas.FetchProviderBaseEvent | None:
    """
    Parse Base Event Node
    ex: <base_event base_event_id="291" sell_mode="online" title="Camela en concierto">
    """
    if node.tag != "base_event":
        return None

    events = [_parse_event(event_node) for event_node in node]

    return schemas.FetchProviderBaseEvent(
        events=[e for e in events if e],
        **node.attrib,  # type: ignore
    )


def _parse_event(node: etree._Element) -> schemas.FetchProviderEvent | None:
    """
    Parse Event Node
    ex: <event
        event_start_date="2021-06-30T21:00:00" event_end_date="2021-06-30T22:00:00"
        event_id="291" sell_from="2020-07-01T00:00:00" sell_to="2021-06-30T20:00:00" sold_out="false">
    """
    if node.tag != "event":
        return None

    zones = [_parse_event_zone(zone_node) for zone_node in node]

    return schemas.FetchProviderEvent(
        zones=[z for z in zones if z],
        **node.attrib,  # type: ignore
    )


def _parse_event_zone(node: etree._Element) -> schemas.FetchProviderEventZone | None:
    """
    Parse Zone Node
    ex: <zone zone_id="40" capacity="243" price="20.00" name="Platea" numbered="true"/>
    """
    if node.tag != "zone":
        return None

    return schemas.FetchProviderEventZone(
        **node.attrib,  # type: ignore
    )


async def fetch_provider_event_data(events_api_url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(events_api_url)
    return response.content


def parse_provider_event_data(content: str) -> list[schemas.FetchProviderBaseEvent]:
    """Parse Provider XML events response and return a Data Model"""
    data = etree.fromstring(content)
    raw_provider_base_events = [_parse_base_event(base_event_node) for base_event_node in data[0]]
    return [be for be in raw_provider_base_events if be]
