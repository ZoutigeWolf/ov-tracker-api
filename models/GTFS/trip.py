from sqlmodel import Field, SQLModel

from enums import WheelchairAccesibility, BikeAccesibility

class TripGTFS(SQLModel, table=True):
    __tablename__ = "gtfs_trips" # type: ignore

    id: str = Field(primary_key=True)
    realtime_id: str = Field()
    service_id: str = Field()
    route_id: str = Field(foreign_key="gtfs_routes.id")
    shape_id: str | None = Field()
    block_id: str | None = Field()
    headsign: str | None = Field()
    short_name: str | None = Field()
    long_name: str | None = Field()
    direction: int = Field()
    wheelchair_accessible: WheelchairAccesibility = Field(default=WheelchairAccesibility.NoInformation)
    bikes_allowed: BikeAccesibility = Field(default=BikeAccesibility.NoInformation)

    @classmethod
    def parse(cls, **kwargs) -> "TripGTFS":
        return cls(
            id = kwargs["trip_id"],
            realtime_id = kwargs["realtime_trip_id"],
            service_id = kwargs["service_id"],
            route_id = kwargs["route_id"],
            shape_id = kwargs["shape_id"],
            block_id = kwargs["block_id"],
            headsign = kwargs["trip_headsign"],
            short_name = kwargs["trip_short_name"],
            long_name = kwargs["trip_long_name"],
            direction = int(kwargs["direction_id"]),
            wheelchair_accessible = kwargs["wheelchair_accessible"] and WheelchairAccesibility(int(kwargs["wheelchair_accessible"])),
            bikes_allowed = kwargs["bikes_allowed"] and BikeAccesibility(int(kwargs["bikes_allowed"])),
        )
