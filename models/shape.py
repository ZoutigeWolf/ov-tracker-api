from sqlmodel import Field, SQLModel


class Shape(SQLModel, table=True):
    id: str = Field(primary_key=True)
    index: int = Field(primary_key=True)
    latitude: float = Field()
    longitude: float = Field()
    distance_traveled: float | None = Field()

    @classmethod
    def parse(cls, **kwargs) -> "Shape":
        return cls(
            id = kwargs["shape_id"],
            index = int(kwargs["shape_pt_sequence"]),
            latitude = float(kwargs["shape_pt_lat"]),
            longitude = float(kwargs["shape_pt_lon"]),
            distance_traveled = kwargs["shape_dist_traveled"] and float(kwargs["shape_dist_traveled"]),
        )
