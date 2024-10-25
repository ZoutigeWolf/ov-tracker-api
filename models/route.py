from enum import IntEnum
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, Enum

class RouteType(IntEnum):
    Tram = 0
    Subway = 1
    Rail = 2
    Bus = 3
    Ferry = 4
    CableTram = 5
    Aerial = 6
    Funicular = 7
    TrolleyBus = 11
    Monorail = 12


class Route(SQLModel, table=True):
    id: str = Field(primary_key=True)
    agency_id: str = Field()
    code: str | None = Field()
    name: str | None = Field()
    description: str | None = Field()
    type: RouteType = Field()
    color: str | None = Field()
    text_color: str | None = Field()
    url: str | None= Field()

    @classmethod
    def parse(cls, **kwargs) -> "Route":
        return cls(
            id = kwargs["route_id"],
            agency_id = kwargs["agency_id"],
            code = kwargs["route_short_name"],
            name = kwargs["route_long_name"],
            description = kwargs["route_desc"],
            type = kwargs["route_type"] and RouteType(int(kwargs["route_type"])),
            color = kwargs["route_color"],
            text_color = kwargs["route_text_color"],
            url = kwargs["route_url"],
        )
