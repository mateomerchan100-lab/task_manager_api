"""add created_at to tasks

Revision ID: 0c2cb5628cbc
Revises: f5eeb09e6b3b
Create Date: 2026-11-11 14:31:44.855965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c2cb5628cbc'
down_revision: Union[str, Sequence[str], None] = 'f5eeb09e6b3b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TABLE tasks ADD COLUMN created_at TIMESTAMP DEFAULT NOW();")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TABLE tasks DROP COLUMN created_at;")
