from fastapi import APIRouter, Path, Query, Depends
from sqlmodel import Session, func, select

from models.stop import Stop
from database import get_session

router = APIRouter(
    prefix="/api/stops",
    tags=["Stops"]
)


@router.get("/region")
async def get_all_stops_in_region(
    session: Session = Depends(get_session),
    lat: float = Query(ge=-90, le=90),
    lon: float = Query(ge=-180, le=180),
    radius: int = Query(50, gt=0),
) -> list[Stop]:
    stops = session.exec(
        select(Stop)
            .where(
                Stop.latitude is not None \
                and Stop.longitude is not None \
                and func.haversine(lat, lon, Stop.latitude, Stop.longitude) <= radius
            )
    ).all()

    return list(stops)


@router.get("/{stop_id}")
async def get_stop(
    session: Session = Depends(get_session),
    stop_id: str = Path()
) -> Stop | None:
    stop = session.exec(
        select(Stop)
            .where(Stop.id == stop_id)
    ).one_or_none()

    return stop
