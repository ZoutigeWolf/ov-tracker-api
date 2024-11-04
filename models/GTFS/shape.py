from sqlalchemy import Column
from geoalchemy2 import Geometry, WKTElement
from sqlmodel import Field, SQLModel
from typing import Any


class ShapeGTFS(SQLModel):
    __tablename__ = "gtfs_shapes" # type: ignore

    id: str = Field(primary_key=True)
    index: int = Field(primary_key=True)
    line: Geometry | None = Field(sa_column=Column(Geometry(geometry_type="LINESTRING", srid=4326)))
    distance_traveled: float | None = Field()

    @classmethod
    def parse(cls, **kwargs) -> "ShapeGTFS":
        return cls(
            id = kwargs["shape_id"],
            index = int(kwargs["shape_pt_sequence"]),
            line = WKTElement(f"LINESTRING({', '.join(f'{lon} {lat}' for lon, lat in kwargs['points'])})", srid=4326), # type: ignore
            distance_traveled = kwargs["shape_dist_traveled"] and float(kwargs["shape_dist_traveled"]),
        )
