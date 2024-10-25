from sqlmodel import Field, SQLModel


class Agency(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str = Field()
    url: str = Field()
    timezone: str = Field()
    phone_number: str | None = Field()

    @classmethod
    def parse(cls, **kwargs) -> "Agency":
        return cls(
            id = kwargs["agency_id"],
            name = kwargs["agency_name"],
            url = kwargs["agency_url"],
            timezone = kwargs["agency_timezone"],
            phone_number = kwargs["agency_phone"],
        )
