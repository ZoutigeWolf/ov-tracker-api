from pydantic import SkipValidation, field_serializer
from sqlalchemy import Column
from geoalchemy2 import Geometry, WKTElement, WKBElement
from sqlmodel import Field, SQLModel
from shapely.wkb import loads
from typing import Any, Annotated


class ShapeGTFS(SQLModel, table=True):
    __tablename__ = "gtfs_shapes" # type: ignore

    id: str = Field(primary_key=True)
    line: Annotated[WKBElement, SkipValidation] = Field(sa_column=Column(Geometry(geometry_type="LINESTRING", srid=4326)))

    class Config: # type: ignore
        arbitrary_types_allowed = True

    @field_serializer("line")
    def serialize_line(self, line: WKBElement) -> tuple[tuple[float, float], ...]:
        obj = loads(bytes(line.data))
        return tuple(obj.coords)

    @classmethod
    def parse(cls, **kwargs) -> "ShapeGTFS":
        return cls(
            id = kwargs["id"],
            line = WKTElement(kwargs["line_string"], srid=4326), # type: ignore
        )
