from fastapi import APIRouter, Path, Query, Depends
from sqlmodel import Session, func, select, col, and_

from data.realtime import get_realtime_data
from database import get_session
from enums import RouteType


router = APIRouter(
    prefix="/api/map",
    tags=["Map"]
)


@router.get("/positions")
async def get_all_positions_in_region(
    session: Session = Depends(get_session),
    lat: float = Query(ge=-90, le=90),
    lon: float = Query(ge=-180, le=180),
    lat_delta: float = Query(gt=0, le=180),
    lon_delta: float = Query(gt=0, le=360),
    layers: list[RouteType] | None = Query(None),
    limit: int = Query(100, gt=0, le=20000),
    offset: int = Query(0, ge=0)
) -> list:
    if layers is None:
        layers = list(RouteType)
    else:
        layers = [RouteType(l) for l in layers]

    min_lat = lat - (lat_delta / 2)
    max_lat = lat + (lat_delta / 2)
    min_lon = lon - (lon_delta / 2)
    max_lon = lon + (lon_delta / 2)

    return []


@router.get("/stops")
async def get_all_stops_in_region(
    session: Session = Depends(get_session),
    lat: float = Query(ge=-90, le=90),
    lon: float = Query(ge=-180, le=180),
    lat_delta: float = Query(gt=0, le=180),
    lon_delta: float = Query(gt=0, le=360),
    layers: list[RouteType] | None = Query(None),
    limit: int = Query(100, gt=0, le=100),
    offset: int = Query(0, ge=0)
) -> list:
    if layers is None:
        layers = list(RouteType)
    else:
        layers = [RouteType(l) for l in layers]

    min_lat = lat - (lat_delta / 2)
    max_lat = lat + (lat_delta / 2)
    min_lon = lon - (lon_delta / 2)
    max_lon = lon + (lon_delta / 2)

    return []


@router.get("/shapes")
async def get_all_shapes_in_region(
    session: Session = Depends(get_session),
    lat: float = Query(ge=-90, le=90),
    lon: float = Query(ge=-180, le=180),
    lat_delta: float = Query(gt=0, le=180),
    lon_delta: float = Query(gt=0, le=360),
    layers: list[RouteType] | None = Query(None),
    limit: int = Query(100, gt=0, le=100),
    offset: int = Query(0, ge=0)
) -> list:
    if layers is None:
        layers = list(RouteType)
    else:
        layers = [RouteType(l) for l in layers]

    min_lat = lat - (lat_delta / 2)
    max_lat = lat + (lat_delta / 2)
    min_lon = lon - (lon_delta / 2)
    max_lon = lon + (lon_delta / 2)

    return []
