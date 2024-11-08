from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Session, col, select

from enums import WheelchairAccesibility, BikeAccesibility

if TYPE_CHECKING:
    from models.GTFS.stop import StopGTFS
    from models.GTFS.stop_time import StopTimeGTFS
    from models.GTFS.shape import ShapeGTFS
    from models.GTFS.route import RouteGTFS


class TripBase(SQLModel):
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


    def get_detailed(self, session: Session) -> "TripDetailed":
        from models.GTFS import ShapeGTFS, RouteGTFS, StopGTFS, StopTimeGTFS

        shape = session.exec(
            select(ShapeGTFS)
            .where(ShapeGTFS.id == self.shape_id)
            .limit(1)
        ).one()

        route = session.exec(
            select(RouteGTFS)
            .where(RouteGTFS.id == self.route_id)
            .limit(1)
        ).one()

        stops = session.exec(
            select(StopGTFS)
            .join(StopTimeGTFS, col(StopTimeGTFS.trip_id) == self.id)
            .where(StopGTFS.id == StopTimeGTFS.stop_id)
        ).all()

        TripDetailed.model_rebuild()

        return TripDetailed(
            **self.__dict__,
            shape=shape,
            route=route,
            stops=list(stops)
        )


class TripGTFS(TripBase, table=True):
    __tablename__ = "gtfs_trips" # type: ignore

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


class TripDetailed(TripBase):
    shape: "ShapeGTFS" = Field()
    route: "RouteGTFS" = Field()
    stops: list["StopGTFS"] = Field()
