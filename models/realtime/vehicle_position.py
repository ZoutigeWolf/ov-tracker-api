from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime
from datetime import date as dt_date

from enums import VehicleStatus

class VehiclePositionBase(SQLModel):
    id: str = Field(primary_key=True)
    date: dt_date = Field(primary_key=True)
    latitude: float = Field()
    longitude: float = Field()
    stop_index: int = Field()
    status: VehicleStatus = Field()
    trip_id: str = Field()
    stop_id: str | None = Field(default=None)

    @classmethod
    def parse(cls, data) -> "VehiclePositionBase":
        parts = data.id.split(":")
        id = ":".join(parts[1:])
        date = parts[0]
        return cls(
            id=id,
            date=datetime.strptime(date, "%Y-%m-%d").date(),
            latitude=data.vehicle.position.latitude,
            longitude=data.vehicle.position.longitude,
            stop_index=data.vehicle.current_stop_sequence,
            status=VehicleStatus(data.vehicle.current_status),
            trip_id=data.vehicle.trip.trip_id,
            stop_id=data.vehicle.stop_id or None,
        )
