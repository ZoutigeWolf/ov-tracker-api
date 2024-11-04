from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime
from datetime import date as dt_date

from enums import ScheduleRelationship, VehicleStatus

class StopTimeEventBase(SQLModel):
    delay: int | None = Field(default=None)
    time: int | None = Field(default=None)
    uncertainty: int | None = Field(default=None)


    @classmethod
    def parse(cls, data) -> "StopTimeEventBase":
        return data and cls(
            delay=data.delay,
            time=data.time,
            uncertainty=data.uncertainty,
        )
