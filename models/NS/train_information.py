from sqlmodel.main import SQLModel, Field


class TrainInformation(SQLModel):
    trip_id: str = Field()
    type: str = Field()
    parts: list["TrainPart"]

    @classmethod
    def parse(cls, **kwargs) -> "TrainInformation":
        return cls(
            trip_id = str(kwargs["ritnummer"]),
            type = kwargs["type"],
            parts = [TrainPart.parse(**p) for p in kwargs["materieeldelen"]]
        )


from models.NS.train_part import TrainPart
