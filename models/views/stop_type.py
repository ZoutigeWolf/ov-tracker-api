from sqlmodel import SQLModel, Field
from enums import RouteType

class StopType(SQLModel, table=True):
    __tablename__ = "stop_types" # type: ignore

    stop_id: str = Field(primary_key=True, index=True)
    type: RouteType = Field(primary_key=True)
