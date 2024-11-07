import json
from fastapi import APIRouter, Path, Query, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session, func, select, col, and_, text
from geojson import FeatureCollection, Feature
from geoalchemy2.functions import ST_Crosses, ST_Intersects, ST_Within, ST_MakeEnvelope, ST_AsGeoJSON, ST_Centroid, ST_Collect

from data.realtime import get_realtime_data
from database import get_session
from enums import RouteType, LocationType
from models.GTFS import StopGTFS, ShapeGTFS
from models.views import StopType, ShapeType


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
    min_lat: float = Query(ge=-90, le=90),
    min_lon: float = Query(ge=-180, le=180),
    max_lat: float = Query(ge=-90, le=90),
    max_lon: float = Query(ge=-180, le=180),
    layers: list[RouteType] | None = Query(None),
    limit: int = Query(100, gt=0, le=100),
    offset: int = Query(0, ge=0)
):
    if layers is None:
        layers = list(RouteType)
    else:
        layers = [RouteType(l) for l in layers]

    stops = session.exec(
        select(StopGTFS.name, ST_AsGeoJSON(ST_Centroid(ST_Collect(StopGTFS.location))))
        .distinct(col(StopGTFS.name))
        .join(StopType, col(StopType.stop_id) == col(StopGTFS.id))
        .where(and_(
            ST_Within(
                StopGTFS.location,
                ST_MakeEnvelope(min_lat, min_lon, max_lat, max_lon, 4326)
            ),
            col(StopType.type).in_(layers),
            StopGTFS.type == LocationType.StopPlatform
        ))
        .group_by(col(StopGTFS.name), col(StopType.type))
        .offset(offset)
    ).all()

    geodata = FeatureCollection([
        Feature(
            geometry={
                "type": json.loads(location)["type"],
                "coordinates": reversed(json.loads(location)["coordinates"]),
            },
            properties={
                "name": name,
            }
        ) for name, location in stops
    ])

    return JSONResponse(content=geodata)


@router.get("/shapes")
async def get_all_shapes_in_region(
    session: Session = Depends(get_session),
    min_lat: float = Query(ge=-90, le=90),
    min_lon: float = Query(ge=-180, le=180),
    max_lat: float = Query(ge=-90, le=90),
    max_lon: float = Query(ge=-180, le=180),
    layers: list[RouteType] | None = Query(None),
    limit: int = Query(100, gt=0, le=100),
    offset: int = Query(0, ge=0)
):
    if layers is None:
        layers = list(RouteType)
    else:
        layers = [RouteType(l) for l in layers]

    shapes = session.exec(
        select(ShapeGTFS.id, ShapeType.type, ST_AsGeoJSON(ShapeGTFS.line))
        .join(ShapeType, col(ShapeType.shape_id) == col(ShapeGTFS.id))
        .where(and_(
            ST_Within(
                ShapeGTFS.line,
                ST_MakeEnvelope(min_lat, min_lon, max_lat, max_lon, 4326)
            ),
            col(ShapeType.type).in_(layers)
        ))
        .limit(limit)
        .offset(offset)
    ).all()

    geodata = FeatureCollection([
        Feature(
            geometry={
                "type": json.loads(location)["type"],
                "coordinates": reversed(json.loads(location)["coordinates"]),
            },
            properties={
                "id": id,
                "type": type,
            }
        ) for id, type, location in shapes
    ])

    return JSONResponse(content=geodata)
