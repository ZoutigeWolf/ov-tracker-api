"""transfer_fk_delete

Revision ID: 6f4e2a27d3c1
Revises: a4ad5b2eeb59
Create Date: 2024-11-05 01:39:04.203610

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f4e2a27d3c1'
down_revision: Union[str, None] = 'a4ad5b2eeb59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('gtfs_transfers_to_stop_id_fkey', 'gtfs_transfers', type_='foreignkey')
    op.drop_constraint('gtfs_transfers_from_stop_id_fkey', 'gtfs_transfers', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('gtfs_transfers_from_stop_id_fkey', 'gtfs_transfers', 'gtfs_stops', ['from_stop_id'], ['id'])
    op.create_foreign_key('gtfs_transfers_to_stop_id_fkey', 'gtfs_transfers', 'gtfs_stops', ['to_stop_id'], ['id'])
    # ### end Alembic commands ###