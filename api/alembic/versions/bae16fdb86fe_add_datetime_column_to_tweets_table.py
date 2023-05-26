"""add dateTime column to Tweets table

Revision ID: bae16fdb86fe
Revises: 43e0345c9108
Create Date: 2023-05-26 13:17:03.310734

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = 'bae16fdb86fe'
down_revision = '43e0345c9108'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop the update_date table
    op.drop_table('update_date')

    # Add the dateTime column to the tweets table
    op.add_column('tweets', sa.Column('dateTime', sa.String(), nullable=True))


def downgrade() -> None:
    # Remove the dateTime column from the tweets table
    op.drop_column('tweets', 'dateTime')

    # Create the update_date table
    op.create_table(
        'update_date',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint('id', name='update_date_pkey')
    )
