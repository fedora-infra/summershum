"""Drop old package/release columns.

Revision ID: 3be543c95db4
Revises: 4f09001b34e6
Create Date: 2015-05-07 11:05:06.166663

"""

# revision identifiers, used by Alembic.
revision = '3be543c95db4'
down_revision = '4f09001b34e6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # Remove the old columns
    try:
        op.drop_column('files', 'tarball')
        op.drop_column('files', 'tar_sum')
        op.drop_column('files', 'pkg_name')
    except sa.exc.OperationalError:
        # Can't drop columns on sqlite.  oh well..
        pass

def downgrade():
    pass
