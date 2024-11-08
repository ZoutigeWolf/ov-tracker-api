from fastapi import APIRouter, Depends, Path, Query
from sqlmodel import Session, select

from database import get_session
from models.GTFS.stop_time import StopTimeGTFS
from models.GTFS.trip import TripGTFS


router = APIRouter(
    prefix="/api/trips",
    tags=["Trips"]
)


@router.get("")
async def get_all_trips(
    session: Session = Depends(get_session),
    limit: int = Query(100, gt=0, le=100),
    offset: int = Query(0, ge=0)
):
    trips = session.exec(
        select(TripGTFS)
        .limit(limit)
        .offset(offset)
    )

    return trips


@router.get("/{trip_id}")
async def get_trip(
    session: Session = Depends(get_session),
    trip_id: str = Path(),
    detailed: bool = Query(False)
):
    trip = session.exec(
        select(TripGTFS)
        .where(TripGTFS.id == trip_id)
        .limit(1)
    ).one_or_none()

    if detailed and trip is not None:
        trip = trip.get_detailed(session)

    return trip and trip.model_dump()


@router.get("/{trip_id}/times")
async def get_trip_times(
    session: Session = Depends(get_session),
    trip_id: str = Path(),
    detailed: bool = Query(False)
):
    trips = session.exec(
        select(StopTimeGTFS)
        .where(StopTimeGTFS.trip_id == trip_id)
    ).all()

    if detailed:
        trips = [t.get_detailed(session) for t in trips]

    return trips
