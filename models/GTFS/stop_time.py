from sqlmodel import Field, SQLModel, Session, select, col
from datetime import datetime, time

from utils.time import parse_time
from enums import PickupType, DropOffType, Timepoint
from models.GTFS.stop import StopGTFS
from models.GTFS.trip import TripGTFS
from models.GTFS.route import RouteGTFS


class StopTimeBase(SQLModel):
    trip_id: str = Field(primary_key=True, foreign_key="gtfs_trips.id")
    stop_index: int = Field(primary_key=True)
    stop_id: str = Field(index=True)
    stop_headsign: str | None = Field()
    arrival: time = Field()
    departure: time = Field()
    pickup_type: PickupType = Field(default=PickupType.Scheduled)
    drop_off_type: DropOffType = Field(default=DropOffType.Scheduled)
    timepoint: Timepoint = Field(default=Timepoint.Exact)
    shape_dist_traveled: float | None = Field()
    fare_units_traveled: int | None = Field()

    def get_detailed(self) -> "StopTimeDetailed":
        from database import engine
        with Session(engine) as session:
            stop = session.exec(
                select(StopGTFS)
                .where(col(StopGTFS.id) == self.stop_id)
            ).one()

            trip = session.exec(
                select(TripGTFS)
                .where(col(TripGTFS.id) == self.trip_id)
            ).one()

            route = session.exec(
                select(RouteGTFS)
                .where(col(RouteGTFS.id) == trip.route_id)
            ).one()

        return StopTimeDetailed(
            **self.__dict__,
            stop=stop,
            trip=trip,
            route=route
        )


class StopTimeGTFS(StopTimeBase, table=True):
    __tablename__ = "gtfs_stop_times" # type: ignore

    @classmethod
    def parse(cls, **kwargs) -> "StopTimeGTFS":
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

class StopTimeDetailed(StopTimeBase):
    stop: StopGTFS
    trip: TripGTFS
    route: RouteGTFS
