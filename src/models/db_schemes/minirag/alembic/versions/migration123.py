"""Initial schema

Revision ID: initial_schema
Revises: None
Create Date: 2025-09-13 18:25:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'initial_schema'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create alembic_version table first
    op.execute("""
        CREATE TABLE IF NOT EXISTS alembic_version (
            version_num VARCHAR(32) NOT NULL,
            CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
        )
    """)
    
    # Drop existing tables if they exist
    op.execute('DROP TABLE IF EXISTS chunks CASCADE')
    op.execute('DROP TABLE IF EXISTS assets CASCADE')
    op.execute('DROP TABLE IF EXISTS projects CASCADE')

    # Create tables
    op.create_table(
        'projects',
        sa.Column('project_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('project_uuid', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('project_id')
    )

    # ...existing code...

def downgrade() -> None:
    op.drop_table('chunks')
    op.drop_table('assets')
    op.drop_table('projects')
    op.execute('DROP TABLE IF EXISTS alembic_version')