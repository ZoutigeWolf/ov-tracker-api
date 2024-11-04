from sqlmodel import Field, SQLModel

from enums import RouteType


class RouteGTFS(SQLModel, table=True):
    __tablename__ = "gtfs_routes" # type: ignore

    id: str = Field(primary_key=True)
    agency_id: str = Field(foreign_key="gtfs_agencies.id")
    code: str | None = Field()
    name: str | None = Field()
    description: str | None = Field()
    type: RouteType = Field()
    color: str | None = Field()
    text_color: str | None = Field()
    url: str | None= Field()

    @classmethod
    def parse(cls, **kwargs) -> "RouteGTFS":
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
