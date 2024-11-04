from fastapi import APIRouter, Path, Query, Depends
from sqlmodel import Session, func, select, col, and_

from database import get_session

router = APIRouter(
    prefix="/api/stops",
    tags=["Stops"]
)


@router.get("")
async def get_all_stops(
    session: Session = Depends(get_session),
    limit: int = Query(100, gt=0, le=100),
    offset: int = Query(0, ge=0)
) -> list:
    return []


@router.get("/{stop_id}")
async def get_stop(
    session: Session = Depends(get_session),
    stop_id: str = Path(),
    detailed: bool = Query(False)
) -> None:
    return None
