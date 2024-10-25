from enum import IntEnum
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, Enum


class WheelchairBoarding(IntEnum):
    NoInformation = 0
    SomeVehicles = 1
    NotPossible = 2


class LocationType(IntEnum):
    StopPlatform = 0
    Station = 1
    EntranceExit = 2
    GenericNode = 3
    BoardingArea = 4


class Stop(SQLModel, table=True):
    id: str = Field(primary_key=True)
    code: str | None = Field()
    name: str | None = Field()
    latitude: float | None = Field()
    longitude: float | None = Field()
    type: LocationType = Field(default=LocationType.StopPlatform)
    parent: str | None = Field()
    timezone: str | None = Field()
    wheelchair_boarding: WheelchairBoarding = Field(default=WheelchairBoarding.NoInformation)
    platform_code: str | None = Field()
    zone_id: str | None = Field()

    @classmethod
    def parse(cls, **kwargs) -> "Stop":
        return cls(
            id = kwargs["stop_id"],
            code = kwargs["stop_code"],
            name = kwargs["stop_name"],
            latitude = kwargs["stop_lat"] and float(kwargs["stop_lat"]),
            longitude = kwargs["stop_lon"] and float(kwargs["stop_lon"]),
            type = kwargs["location_type"] and LocationType(int(kwargs["location_type"])),
            parent = kwargs["parent_station"],
            timezone = kwargs["stop_timezone"],
            wheelchair_boarding = kwargs["wheelchair_boarding"] and WheelchairBoarding(int(kwargs["wheelchair_boarding"])),
            platform_code = kwargs["platform_code"],
            zone_id = kwargs["zone_id"],
        )
