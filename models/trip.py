from sqlmodel import Field, SQLModel
from sqlalchemy import Column, Enum
from enum import IntEnum


class WheelchairAccesiblity(IntEnum):
    NoInformation = 0
    AtLeastOne = 1
    NotPossible = 2


class BikeAccesiblity(IntEnum):
    NoInformation = 0
    AtLeastOne = 1
    NotPossible = 2


class Trip(SQLModel, table=True):
    id: str = Field(primary_key=True)
    realtime_id: str = Field()
    service_id: str = Field()
    route_id: str = Field()
    headsign: str | None = Field()
    short_name: str | None = Field()
    long_name: str | None = Field()
    direction: int = Field()
    block_id: str | None = Field()
    shape_id: str | None = Field()
    weelchair_accessible: WheelchairAccesiblity = Field(default=WheelchairAccesiblity.NoInformation)
    bikes_allowed: BikeAccesiblity = Field(default=BikeAccesiblity.NoInformation)

    @classmethod
    def parse(cls, **kwargs) -> "Trip":
        return cls(
            id = kwargs["trip_id"],
            realtime_id = kwargs["realtime_trip_id"],
            service_id = kwargs["service_id"],
            route_id = kwargs["route_id"],
            headsign = kwargs["trip_headsign"],
            short_name = kwargs["trip_short_name"],
            long_name = kwargs["trip_long_name"],
            direction = int(kwargs["direction_id"]),
            block_id = kwargs["block_id"],
            shape_id = kwargs["shape_id"],
            weelchair_accessible = kwargs["wheelchair_accessible"] and WheelchairAccesiblity(int(kwargs["wheelchair_accessible"])),
            bikes_allowed = kwargs["bikes_allowed"] and BikeAccesiblity(int(kwargs["bikes_allowed"])),
        )
