from geoalchemy2.elements import WKBElement
from geojson import Feature, Point
from pydantic import SkipValidation, field_serializer
from sqlalchemy import Column
from geoalchemy2 import WKTElement, Geometry
from sqlmodel import Field, SQLModel, Session, select, col
from shapely.wkb import loads
from typing import Any, Annotated

from enums import WheelchairBoarding, LocationType
from models.GTFS.agency import AgencyGTFS
from models.GTFS.route import RouteGTFS
from models.GTFS.trip import TripGTFS
from models.views import StopRoute

class StopBase(SQLModel):
    id: str = Field(primary_key=True)
    code: str | None = Field()
    name: str | None = Field()
    location: Annotated[WKBElement, SkipValidation] = Field(sa_column=Column(Geometry(geometry_type="POINT", srid=4326)))
    type: LocationType = Field(default=LocationType.StopPlatform)
    parent_id: str | None = Field()
    timezone: str | None = Field()
    wheelchair_boarding: WheelchairBoarding = Field(default=WheelchairBoarding.NoInformation)
    platform_code: str | None = Field()
    zone_id: str | None = Field()

    class Config: # type: ignore
        arbitrary_types_allowed = True

    @field_serializer("location")
    def serialize_location(self, location: WKBElement) -> tuple[float, float]:
        obj = loads(bytes(location.data))
        return obj.coords[0]

    def get_detailed(self) -> "StopDetailed":
        from database import engine
        with Session(engine) as session:
            routes = session.exec(
                select(RouteGTFS)
                .join(StopRoute, col(StopRoute.route_id) == col(RouteGTFS.id))
                .where(col(StopRoute.stop_id) == self.id)
            ).all()

            agencies = session.exec(
                select(AgencyGTFS)
                .distinct()
                .where(col(AgencyGTFS.id).in_([r.agency_id for r in routes]))
            ).all()

        return StopDetailed(
            **self.__dict__,
            agencies=list(agencies),
            routes=list(routes)
        )

class StopGTFS(StopBase, table=True):
    __tablename__ = "gtfs_stops" # type: ignore

    @classmethod
    def parse(cls, **kwargs) -> "StopGTFS":
        return cls(
            id = kwargs["stop_id"],
            code = kwargs["stop_code"],
            name = kwargs["stop_name"],
            location = WKTElement(f"POINT({kwargs['stop_lat']} {kwargs['stop_lon']})", srid=4326), # type: ignore
            type = kwargs["location_type"] and LocationType(int(kwargs["location_type"])),
            parent_id = kwargs["parent_station"],
            timezone = kwargs["stop_timezone"],
            wheelchair_boarding = kwargs["wheelchair_boarding"] and WheelchairBoarding(int(kwargs["wheelchair_boarding"])),
            platform_code = kwargs["platform_code"],
            zone_id = kwargs["zone_id"],
        )


class StopDetailed(StopBase):
    agencies: list[AgencyGTFS] = Field()
    routes: list[RouteGTFS] = Field()
