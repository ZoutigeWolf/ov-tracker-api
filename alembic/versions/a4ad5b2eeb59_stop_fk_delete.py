"""stop_fk_delete

Revision ID: a4ad5b2eeb59
Revises: bc2968bcbb5a
Create Date: 2024-11-05 01:32:58.021286

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4ad5b2eeb59'
down_revision: Union[str, None] = 'bc2968bcbb5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('gtfs_stop_times_stop_id_fkey', 'gtfs_stop_times', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('gtfs_stop_times_stop_id_fkey', 'gtfs_stop_times', 'gtfs_stops', ['stop_id'], ['id'])
    # ### end Alembic commands ###