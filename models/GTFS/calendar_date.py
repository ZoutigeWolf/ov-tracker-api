from sqlmodel import Field, SQLModel
from datetime import datetime

from enums import ExceptionType

class CalendarDateGTFS(SQLModel):
    __tablename__ = "gtfs_calendar_dates" # type: ignore

    service_id: str = Field(primary_key=True)
    date: datetime = Field(primary_key=True)
    exception_type: ExceptionType = Field()

    @classmethod
    def parse(cls, **kwargs) -> "CalendarDateGTFS":
        return cls(
            service_id = kwargs["service_id"],
            date = datetime.strptime(kwargs["date"], "%Y%m%d"),
            exception_type = kwargs["exception_type"] and ExceptionType(int(kwargs["exception_type"]))
        )
