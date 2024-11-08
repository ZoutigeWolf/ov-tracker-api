from sqlmodel.main import SQLModel, Field


class TrainPart(SQLModel):
    image: str = Field()
    width: int = Field()
    height: int = Field()

    @classmethod
    def parse(cls, **kwargs) -> "TrainPart":
        return cls(
            image = kwargs["afbeelding"],
            width = int(kwargs["breedte"]),
            height = int(kwargs["hoogte"])
        )
