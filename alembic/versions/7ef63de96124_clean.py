"""clean

Revision ID: 7ef63de96124
Revises: 22c672ff6512
Create Date: 2025-04-03 14:21:55.612976

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ef63de96124'
down_revision: Union[str, None] = '22c672ff6512'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('battery_history', sa.Column('event_id', sa.UUID(), nullable=False))
    op.drop_column('battery_history', 'id')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('battery_history', sa.Column('id', sa.UUID(), autoincrement=False, nullable=False))
    op.drop_column('battery_history', 'event_id')
    # ### end Alembic commands ###
