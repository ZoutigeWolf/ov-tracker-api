import os
import requests
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlmodel import Session, select

from database import get_session
from models.GTFS.trip import TripGTFS
from models.NS.train_information import TrainInformation

API_KEY = os.getenv("NS_API_KEY")

router = APIRouter(
    prefix="/api/ns",
    tags=["NS API"]
)

@router.get("/trains/{train_id}")
async def get_train(
    session: Session = Depends(get_session),
    train_id: str = Path(),
):
    res = requests.get(
        f"https://gateway.apiportal.ns.nl/virtual-train-api/v1/trein/{train_id}",
        headers={
            "Ocp-Apim-Subscription-Key": API_KEY
        }
    )

    if res.status_code != 200:
        raise HTTPException(status_code=404, detail="Train not found")

    info = TrainInformation.parse(**res.json())

    return info
