import os
import sys
from geoalchemy2 import WKTElement
from sqlmodel import Session, select, text
from typing import Callable, Generator
import csv
import pandas as pd

from database import engine
from models.GTFS import AgencyGTFS, CalendarDateGTFS, RouteGTFS, ShapeGTFS, StopGTFS, StopTimeGTFS, TransferGTFS, TripGTFS

MODELS = [
    ["agency", AgencyGTFS.parse],
    ["calendar_dates", CalendarDateGTFS.parse],
    ["shapes", ShapeGTFS.parse],
    ["stops", StopGTFS.parse],
    ["routes", RouteGTFS.parse],
    ["trips", TripGTFS.parse],
    ["stop_times", StopTimeGTFS.parse],
    ["transfers", TransferGTFS.parse],
]

def import_gtfs(dir: str):
    with Session(engine) as session:
        for name in [m[0] for m in MODELS]:
            f_name = f"{name}.txt"
            if not os.path.isfile(os.path.join(dir, f_name)):
                continue


            cls = [m[1] for m in MODELS if m[0] == name][0]

            get_func = parse_file

            if name == "shapes":
                get_func = parse_shapes

            i = 0
            for obj in get_func(os.path.join(dir, f_name), cls):
                session.add(obj)

                i += 1

                if i == 100_000:
                    print("Committing...")
                    session.commit()
                    i = 0

            if i > 0:
                print("Committing...")
                session.commit()

    print("Done")


def parse_file(path: str, cls: Callable) -> Generator:
    with open(path) as f:
        print(f"Reading {path}")
        data = [l.replace("\n", "") for l in f.readlines()]
        reader = csv.reader(data, delimiter=",", quotechar="\"")

    name = path.split("/")[-1].split(".")[0]

    keys = next(reader)

    print(f"Rows: {len(data) - 1}")

    for i, row in enumerate(reader):
        obj = cls(**{
            keys[i]: v or None for i, v in enumerate(row)
        })

        p = (i + 1) / (len(data) - 1) * 100

        print(f"{name}: {i + 1} / {len(data) - 1} [{p:.2f}%]: {row}")

        yield obj


def parse_shapes(path: str, cls: Callable) -> Generator:
    with open(path) as f:
        print(f"Reading {path}")
        data = pd.read_csv(path)

    for i, (id, group) in enumerate(data.groupby("shape_id")):
        group = group.sort_values("shape_pt_sequence")

        points = group[["shape_pt_lon", "shape_pt_lat"]].values
        line_string = f"LINESTRING({', '.join(f'{lon} {lat}' for lon, lat in points)})"

        obj = cls(
            id=str(id),
            line_string=line_string
        )

        len_data = data['shape_id'].nunique()

        p = (i + 1) / (len_data) * 100

        print(f"shapes: {i + 1} / {len_data} [{p:.2f}%]: {len(points)} points")

        yield obj


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Usage: python import_data.py <gtfs_dir>")
        exit(1)

    dir = sys.argv[1]

    if not os.path.isdir(dir):
        print(f"Directory \"{dir}\" not found")
        exit(1)

    import_gtfs(dir)
