"""gtfs

Revision ID: a8d52d2f6519
Revises:
Create Date: 2024-10-30 14:49:58.182229

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8d52d2f6519'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table("agency", "gtfs_agencies")
    op.rename_table("calendardate", "gtfs_calendar_dates")
    op.rename_table("route", "gtfs_routes")
    op.rename_table("shape", "gtfs_shapes")
    op.rename_table("stop", "gtfs_stops")
    op.rename_table("stoptime", "gtfs_stop_times")
    op.rename_table("transfer", "gtfs_transfers")
    op.rename_table("trip", "gtfs_trips")


def downgrade() -> None:
    op.rename_table("gtfs_agencies", "agency")
    op.rename_table("gtfs_calendar_dates", "calendardate")
    op.rename_table("gtfs_routes", "route")
    op.rename_table("gtfs_shapes", "shape")
    op.rename_table("gtfs_stops", "stop")
    op.rename_table("gtfs_stop_times", "stoptime")
    op.rename_table("gtfs_transfers", "transfer")
    op.rename_table("gtfs_trips", "trip")
