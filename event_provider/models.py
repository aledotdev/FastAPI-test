import enum
from datetime import datetime, time

from sqlalchemy import Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

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
    base_event_id: Mapped[int] = mapped_column(primary_key=True)
    sell_mode: Mapped[str] = mapped_column(Enum(SellModeEnum))
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    organizer_company_id: Mapped[int]

    provider: Mapped["Provider"] = relationship("Provider")


class ProviderEvent(DBBase):
    __tablename__ = "provider_event"

    id: Mapped[int] = mapped_column(primary_key=True)
    provider_id: Mapped[int] = mapped_column(ForeignKey("provider.id"))
    provider_base_event_id: Mapped[int] = mapped_column(ForeignKey("provider_base_event.id"))
    event_id: Mapped[int] = mapped_column(primary_key=True)
    event_start_date: Mapped[datetime]
    event_start_time: Mapped[time]
    event_end_date: Mapped[datetime]
    event_end_time: Mapped[time]
    sell_from: Mapped[datetime]
    sell_to: Mapped[datetime]
    sold_out: Mapped[bool] = mapped_column(default=False)

    provider: Mapped["Provider"] = relationship("Provider")
    zones: Mapped[list["ProviderEventZone"]] = relationship()


class ProviderEventZone(DBBase):
    __tablename__ = "provider_event_zone"

    id: Mapped[int] = mapped_column(primary_key=True)
    provider_event_id: Mapped[int] = mapped_column(ForeignKey("provider_event.id"))
    zone_id: Mapped[int] = mapped_column(primary_key=True)
    capacity: Mapped[int]
    price: Mapped[float]
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    numbered: Mapped[bool] = mapped_column(default=False)

    provider_event: Mapped["ProviderEvent"] = relationship(back_populates="zones")

    __table_args__ = (UniqueConstraint("provider_event_id", "zone_id", name="_provider_event_zone_uc"),)
