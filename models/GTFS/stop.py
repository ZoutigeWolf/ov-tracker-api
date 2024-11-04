from pydantic import SkipValidation, field_validator
from sqlalchemy import Column
from geoalchemy2 import Geometry, WKTElement
from sqlmodel import Field, SQLModel
from typing import Any, Annotated

from enums import WheelchairBoarding, LocationType


class StopGTFS(SQLModel, table=True):
    __tablename__ = "gtfs_stops" # type: ignore

    id: str = Field(primary_key=True)
    code: str | None = Field()
    name: str | None = Field()
    location: Annotated[Geometry, SkipValidation] = Field(sa_column=Column(Geometry(geometry_type="POINT", srid=4326)))
    type: LocationType = Field(default=LocationType.StopPlatform)
    parent_id: str | None = Field()
    timezone: str | None = Field()
    wheelchair_boarding: WheelchairBoarding = Field(default=WheelchairBoarding.NoInformation)
    platform_code: str | None = Field()
    zone_id: str | None = Field()

    class Config: # type: ignore
        arbitrary_types_allowed = True

    @classmethod
    def parse(cls, **kwargs) -> "StopGTFS":
        return cls(
            id = kwargs["stop_id"],
            code = kwargs["stop_code"],
            name = kwargs["stop_name"],
            location = WKTElement(f"POINT({kwargs['stop_lat']}, {kwargs['stop_lon']})", srid=4326), # type: ignore
            type = kwargs["location_type"] and LocationType(int(kwargs["location_type"])),
            parent_id = kwargs["parent_station"],
            timezone = kwargs["stop_timezone"],
            wheelchair_boarding = kwargs["wheelchair_boarding"] and WheelchairBoarding(int(kwargs["wheelchair_boarding"])),
            platform_code = kwargs["platform_code"],
            zone_id = kwargs["zone_id"],
        )
