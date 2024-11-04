from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime
from datetime import date as dt_date

from enums import ScheduleRelationship, VehicleStatus

class StopTimeUpdateBase(SQLModel):
    stop_id: str = Field(primary_key=True)
    stop_index: int = Field(primary_key=True)
    arrival: "StopTimeEventBase | None" = Field(default=None)
    departure: "StopTimeEventBase | None" = Field(default=None)

    @classmethod
    def parse(cls, data) -> "StopTimeUpdateBase":
        return cls(
            stop_id=data.stop_id,
            stop_index=data.stop_sequence,
            arrival=StopTimeEventBase.parse(data.arrival),
            departure=StopTimeEventBase.parse(data.arrival),
        )


from models.realtime.stop_time_event import StopTimeEventBase
