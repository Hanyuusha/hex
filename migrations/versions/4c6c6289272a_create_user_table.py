"""create user table

Revision ID: 4c6c6289272a
Revises: 
Create Date: 2022-05-12 07:55:17.474738

"""
import uuid

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '4c6c6289272a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('first_name', sa.String(50), nullable=False),
        sa.Column('second_name', sa.String(50), nullable=False),
    )


def downgrade():
    op.drop_index('users')
