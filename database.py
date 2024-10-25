import os
import csv
from typing import AsyncGenerator
import aiofiles
from sqlmodel import SQLModel, Session, create_engine

from models import Agency, CalendarDate, Route, Shape, Stop, StopTime, Transfer, Trip

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

engine = create_engine(
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

def get_session():
    with Session(engine) as session:
        yield session

MODELS = {
    "agency": Agency.parse,
    "calendar_dates": CalendarDate.parse,
    "routes": Route.parse,
    "shapes": Shape.parse,
    "stops": Stop.parse,
    "stop_times": StopTime.parse,
    "transfers": Transfer.parse,
    "trips": Trip.parse
}


async def import_gtfs(dir: str):
    with Session(engine) as session:
        for f_name in os.listdir(dir):
            if f_name.split(".")[0] not in MODELS:
                continue

            i = 0
            async for obj in parse_file(os.path.join(dir, f_name)):
                session.add(obj)
                i += 1

                if i == 100_000:
                    print("Committing...")
                    session.commit()
                    i = 0

            if i > 0:
                print("Committing...")
                session.commit()


async def parse_file(path: str) -> AsyncGenerator:
    async with aiofiles.open(path) as f:
        print(f"Reading {path}")
        data = [l.replace("\n", "") for l in await f.readlines()]
        reader = csv.reader(data, delimiter=",", quotechar="\"")

    name = path.split("/")[-1].split(".")[0]

    keys = next(reader)

    cls = MODELS.get(name)

    if not cls:
        raise ValueError(f"Model not found for {name}")

    print(f"Rows: {len(data) - 1}")

    for i, row in enumerate(reader):
        yield cls(**{
            keys[i]: v or None for i, v in enumerate(row)
        })

        p = (i + 1) / (len(data) - 1) * 100

        print(f"{name}: {i + 1} / {len(data) - 1} [{p:.2f}%]: {row}")
