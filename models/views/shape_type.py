from sqlmodel import SQLModel, Field
from enums import RouteType

class ShapeType(SQLModel, table=True):
    __tablename__ = "shape_types" # type: ignore

    shape_id: str = Field(primary_key=True, index=True)
    type: RouteType = Field(primary_key=True)
