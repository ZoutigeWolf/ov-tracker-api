import os
import requests
import logging

logger = logging.getLogger("uvicorn.error")

FILES = [
    "https://gtfs.ovapi.nl/nl/vehiclePositions.pb",
    "https://gtfs.ovapi.nl/nl/tripUpdates.pb",
    "https://gtfs.ovapi.nl/nl/trainUpdates.pb"
]


def fetch(dir: str):
    for url in FILES:
        file = url.split("/")[-1]
        res = requests.get(url)

        if res.status_code != 200:
            logger.info(f"Failed to fetch: {file}, status: {res.status_code}")
            if res.status_code == 429:
                return

            continue

        with open(os.path.join(dir, file), "wb") as f:
            f.write(res.content)

        logger.info(f"Fetched {file}")
