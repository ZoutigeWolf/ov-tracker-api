import datetime
from enum import IntEnum
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, Enum
from datetime import datetime, time

from utils.time import parse_time


class PickupType(IntEnum):
    Scheduled = 0
    NoPickup = 1
    PhoneAgency = 2
    CoordinateWithDriver = 3


class DropOffType(IntEnum):
    Scheduled = 0
    NoDropOff = 1
    PhoneAgency = 2
    CoordinateWithDriver = 3


class Timepoint(IntEnum):
    Approximate = 0
    Exact = 1


class StopTime(SQLModel, table=True):
    trip_id: str = Field(primary_key=True)
    stop_index: int = Field(primary_key=True)
    stop_id: str | None = Field()
    stop_headsign: str | None = Field()
    arrival: time = Field()
    departure: time = Field()
    pickup_type: PickupType = Field(default=PickupType.Scheduled)
    drop_off_type: DropOffType = Field(default=DropOffType.Scheduled)
    timepoint: Timepoint = Field(default=Timepoint.Exact)
    shape_dist_traveled: float | None = Field()
    fare_units_traveled: int | None = Field()

    @classmethod
    def parse(cls, **kwargs) -> "StopTime":
        return cls(
            trip_id = kwargs["trip_id"],
            stop_index = int(kwargs["stop_sequence"]),
            stop_id = kwargs["stop_id"],
            stop_headsign = kwargs["stop_headsign"],
            arrival = kwargs["arrival_time"] and parse_time(kwargs["arrival_time"]),
            departure = kwargs["departure_time"] and parse_time(kwargs["departure_time"]),
            pickup_type = kwargs["pickup_type"] and PickupType(int(kwargs["pickup_type"])),
            drop_off_type = kwargs["drop_off_type"] and DropOffType(int(kwargs["drop_off_type"])),
            timepoint = kwargs["timepoint"] and Timepoint(int(kwargs["timepoint"])),
            shape_dist_traveled = kwargs["shape_dist_traveled"] and float(kwargs["shape_dist_traveled"]),
            fare_units_traveled = kwargs["fare_units_traveled"] and int(kwargs["fare_units_traveled"]),
        )
        datetime.datetime.now().time()
