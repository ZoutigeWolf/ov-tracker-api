from fastapi import APIRouter, HTTPException, Path, Query, Depends
from fastapi.responses import JSONResponse
from geoalchemy2.functions import ST_DistanceSpheroid, ST_MakePoint, ST_SetSRID
from sqlmodel import Session, func, select, col, and_
from sqlalchemy import func
from datetime import datetime

from database import get_session
from models.GTFS.calendar_date import CalendarDateGTFS
from models.GTFS.stop import StopDetailed, StopGTFS
from models.GTFS import StopTimeGTFS
from models.GTFS.trip import TripGTFS
from models.views.stop_type import StopType

router = APIRouter(
    prefix="/api/stops",
    tags=["Stops"]
)


@router.get("")
async def get_all_stops(
    session: Session = Depends(get_session),
    name: str | None = Query(None),
    search: bool = Query(False),
    lat: float | None = Query(None, ge=-90, le=90),
    lon: float | None = Query(None, ge=-180, le=180),
    detailed: bool = Query(False),
    limit: int = Query(100, gt=0, le=100),
    offset: int = Query(0, ge=0)
):
    if (lat is None) != (lon is None):
        raise HTTPException(status_code=400, detail="Only part of coordinate supplied")

    if not name and search:
        return []

    q = select(StopGTFS)

    if name is not None:
        if search:
            q = (
                q.where(col(StopGTFS.name).ilike(f"%{name}%"))
            )
        else:
            q = q.where(StopGTFS.name == name)

    if lat is not None:
        q = q.order_by(ST_DistanceSpheroid(
            StopGTFS.location,
            ST_SetSRID(ST_MakePoint(lon, lat), 4326)
        ))

    stops = session.exec(
        q
        .limit(limit)
        .offset(offset)
    ).all()

    if detailed:
        stops = list(map(lambda s: s.get_detailed(), stops))

    return [s.model_dump() for s in stops]


@router.get("/{stop_id}")
async def get_stop(
    session: Session = Depends(get_session),
    stop_id: str = Path(),
    detailed: bool = Query(False)
):
    stop = session.exec(
        select(StopGTFS)
        .where(StopGTFS.id == stop_id)
    ).one_or_none()

    if detailed and stop is not None:
        stop = stop.get_detailed()

    return stop and stop.model_dump()

@router.get("/{stop_id}/times")
async def get_stop_times(
    session: Session = Depends(get_session),
    stop_id: str = Path(),
    detailed: bool = Query(False)
):
    times = session.exec(
        select(StopTimeGTFS)
        .join(TripGTFS, col(TripGTFS.id) == col(StopTimeGTFS.trip_id))
        .join(CalendarDateGTFS, col(CalendarDateGTFS.service_id) == col(TripGTFS.service_id))
        .where(and_(
            StopTimeGTFS.stop_id == stop_id,
            col(StopTimeGTFS.departure) > datetime.now().time(),
            col(CalendarDateGTFS.date) == func.current_date()
        ))
        .order_by(col(StopTimeGTFS.departure))
        .limit(2)
    ).all()

    if detailed:
        times = list(map(lambda t: t.get_detailed(), times))

    return times
