from enum import IntEnum
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, Enum
from datetime import datetime


class ExceptionType(IntEnum):
    Added = 1
    Removed = 2


class CalendarDate(SQLModel, table=True):
    id: str = Field(primary_key=True)
    date: datetime = Field(primary_key=True)
    exception_type: ExceptionType = Field()

    @classmethod
    def parse(cls, **kwargs) -> "CalendarDate":
        return cls(
            id = kwargs["service_id"],
            date = datetime.strptime(kwargs["date"], "%Y%m%d"),
            exception_type = kwargs["exception_type"] and ExceptionType(int(kwargs["exception_type"]))
        )
