"""create date table

Revision ID: 43e0345c9108
Revises: 89cf293436f6
Create Date: 2023-05-26 10:15:39.727282

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43e0345c9108'
down_revision = '89cf293436f6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('update_date',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name='update_date_pkey')
    )


def downgrade() -> None:
    op.drop_table('update_date')
