"""add dateTime column to sentiments

Revision ID: bfd271df40fe
Revises: bae16fdb86fe
Create Date: 2023-05-31 00:25:24.487769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfd271df40fe'
down_revision = 'bae16fdb86fe'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add the dateTime column to the sentiments table
    op.add_column('sentiments', sa.Column('dateTime', sa.String(), nullable=True))


def downgrade() -> None:
    # Remove the dateTime column from the tweets table
    op.drop_column('sentiments', 'dateTime')
