from enum import IntEnum
import uuid
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, Enum


class TransferType(IntEnum):
    Recommended = 0
    Timed = 1
    Minimum = 2
    NotPossible = 3
    InSeat = 4
    ReBoard = 5

class Transfer(SQLModel, table=True):
    id: str = Field(default_factory=uuid.uuid4, primary_key=True)
    from_stop_id: str | None = Field()
    to_stop_id: str | None = Field()
    from_route_id: str | None = Field()
    to_route_id: str  | None = Field()
    from_trip_id: str | None = Field()
    to_trip_id: str | None = Field()
    transfer_type: TransferType = Field(default=TransferType.Recommended)
    min_transfer_time: int | None = Field()

    @classmethod
    def parse(cls, **kwargs) -> "Transfer":
        return cls(
            from_stop_id = kwargs["from_stop_id"],
            to_stop_id = kwargs["to_stop_id"],
            from_route_id = kwargs["from_route_id"],
            to_route_id = kwargs["to_route_id"],
            from_trip_id = kwargs["from_trip_id"],
            to_trip_id = kwargs["to_trip_id"],
            transfer_type = kwargs["transfer_type"] and TransferType(int(kwargs["transfer_type"])),
            min_transfer_time = kwargs["min_transfer_time"] and int(kwargs["min_transfer_time"]),
        )
