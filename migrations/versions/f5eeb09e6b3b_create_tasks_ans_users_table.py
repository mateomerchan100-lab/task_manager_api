"""create tasks ans users table

Revision ID: f5eeb09e6b3b
Revises: 
Create Date: 2026-11-07 19:25:41.465719

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5eeb09e6b3b'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY ,
            title TEXT NOT NULL UNIQUE,
            done BOOLEAN NOT NULL,
            owner TEXT NOT NULL
        )
        """)
    
    op.execute("""
    CREATE INDEX IF NOT EXISTS idx_tasks_owner ON tasks (owner);
""")

    op.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY ,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
        )
        
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
            DROP TABLE IF EXISTS users 
            """)

    op.execute("""
            DROP TABLE IF  EXISTS tasks 
            """)
        
    
    
