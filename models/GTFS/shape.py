from pydantic import SkipValidation, field_validator
from sqlalchemy import Column
from geoalchemy2 import Geometry, WKTElement
from sqlmodel import Field, SQLModel
from typing import Any, Annotated


class ShapeGTFS(SQLModel, table=True):
    __tablename__ = "gtfs_shapes" # type: ignore

    id: str = Field(primary_key=True)
    line: Annotated[Geometry, SkipValidation] = Field(sa_column=Column(Geometry(geometry_type="LINESTRING", srid=4326)))

    class Config: # type: ignore
        arbitrary_types_allowed = True

    @classmethod
    def parse(cls, **kwargs) -> "ShapeGTFS":
        return cls(
            id = kwargs["id"],
            line = WKTElement(kwargs["line_string"], srid=4326), # type: ignore
        )
