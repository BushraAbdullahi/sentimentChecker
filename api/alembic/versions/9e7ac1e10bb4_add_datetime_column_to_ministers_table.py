"""add dateTime column to ministers table

Revision ID: 9e7ac1e10bb4
Revises: bfd271df40fe
Create Date: 2023-06-02 22:02:48.411852

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e7ac1e10bb4'
down_revision = 'bfd271df40fe'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('cabinet_ministers', sa.Column('dateTime', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('cabinet_ministers', 'dateTime')
