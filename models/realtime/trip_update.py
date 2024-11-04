from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime
from datetime import date as dt_date

from enums import ScheduleRelationship, VehicleStatus

class TripUpdateBase(SQLModel):
    id: str = Field(primary_key=True)
    date: dt_date = Field(primary_key=True)
    trip_id: str | None = Field(default=None)
    route_id: str | None = Field(default=None)
    direction: int | None = Field(default=None)
    start_time: datetime | None = Field(default=None)
    schedule_relationship: ScheduleRelationship | None = Field(default=None)
    updates: list["StopTimeUpdateBase"] = Field(default=[])

    @classmethod
    def parse(cls, data) -> "TripUpdateBase":
        parts = data.id.split(":")
        id = ":".join(parts[1:])
        date = parts[0]

        trip = data.trip_update.trip

        return cls(
            id=id,
            date=datetime.strptime(date, "%Y-%m-%d").date(),
            trip_id=trip.trip_id,
            route_id=trip.route_id,
            direction=trip.direction_id,
            start_time=trip.start_date and trip.start_time \
                and datetime.strptime(f"{trip.start_date} {trip.start_time}", "%Y%m%d %H:%M:%S"),
            schedule_relationship=ScheduleRelationship(trip.schedule_relationship),
            updates=[StopTimeUpdateBase.parse(update) for update in data.trip_update.stop_time_update],
        )

from models.realtime.stop_time_update import StopTimeUpdateBase
