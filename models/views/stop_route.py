from sqlmodel import SQLModel, Field
from enums import RouteType

class StopRoute(SQLModel, table=True):
    __tablename__ = "stop_routes" # type: ignore

    stop_id: str = Field(primary_key=True, index=True)
    route_id: str = Field(primary_key=True)
