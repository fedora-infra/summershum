"""Add a packages table.

Revision ID: 15f941de8d61
Revises: None
Create Date: 2015-05-07 10:28:02.798256

"""

# revision identifiers, used by Alembic.
revision = '15f941de8d61'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


def upgrade():
    # Create the new structures
    op.create_table(
        'packages',
        sa.Column('pkg_name', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('pkg_name')
    )
    op.create_table(
        'releases',
        sa.Column('pkg_name', sa.Text(), nullable=False),
        sa.Column('tarball', sa.Text(), nullable=False),
        sa.Column('tar_sum', sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(['pkg_name'], ['packages.pkg_name'], onupdate='CASCADE'),
        sa.PrimaryKeyConstraint('tarball', 'tar_sum'),
        sa.UniqueConstraint('tarball', 'tar_sum')
    )
    op.create_index(op.f('ix_releases_pkg_name'), 'releases', ['pkg_name'], unique=False)


def downgrade():
    pass
