  # pylint: disable=too-few-public-methods

import enum
from datetime import time

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import DBBase


class Provider(DBBase):
    __tablename__ = "provider"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))


class SellModeEnum(enum.Enum):
    offline = 0
    online = 1


class ProviderBaseEvent(DBBase):
    __tablename__ = "provider_base_event"

    id: Mapped[int] = mapped_column(primary_key=True)
    provider_id: Mapped[int] = mapped_column(ForeignKey("provider.id"))
    base_event_id: Mapped[int]
    sell_mode: Mapped[str] = mapped_column(Enum(SellModeEnum))
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    organizer_company_id: Mapped[int]

    provider: Mapped["Provider"] = relationship("Provider")
    events: Mapped[list["ProviderEvent"]] = relationship()

    __table_args__ = (UniqueConstraint("provider_id", "base_event_id", name="_provider_base_event_id_uc"),)


class ProviderEvent(DBBase):
    __tablename__ = "provider_event"

    id: Mapped[int] = mapped_column(primary_key=True)
    provider_id: Mapped[int] = mapped_column(ForeignKey("provider.id"))
    provider_base_event_id: Mapped[int] = mapped_column(ForeignKey("provider_base_event.id"))
    event_id: Mapped[int]

    event_start_date = mapped_column(DateTime(timezone=True))
    event_start_time: Mapped[time]
    event_end_date = mapped_column(DateTime(timezone=True))
    event_end_time: Mapped[time]
    sell_from = mapped_column(DateTime(timezone=True))
    sell_to = mapped_column(DateTime(timezone=True))
    sold_out: Mapped[bool] = mapped_column(Boolean, default=False)

    provider: Mapped["Provider"] = relationship("Provider")
    provider_base_event: Mapped["ProviderBaseEvent"] = relationship(back_populates="events")
    zones: Mapped[list["ProviderEventZone"]] = relationship()

    __table_args__ = (UniqueConstraint("provider_id", "event_id", name="_provider_event_id_uc"),)


class ProviderEventZone(DBBase):
    __tablename__ = "provider_event_zone"

    id: Mapped[int] = mapped_column(primary_key=True)
    provider_id: Mapped[int] = mapped_column(ForeignKey("provider.id"))
    provider_event_id: Mapped[int] = mapped_column(ForeignKey("provider_event.id"))
    zone_id: Mapped[int]
    capacity: Mapped[int]
    price: Mapped[float]
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    numbered: Mapped[bool] = mapped_column(default=False)

    provider: Mapped["Provider"] = relationship("Provider")
    provider_event: Mapped["ProviderEvent"] = relationship(back_populates="zones")

    __table_args__ = (UniqueConstraint("provider_id", "provider_event_id", "zone_id", name="_provider_event_zone_uc"),)
