"""Move packages and release data.

Revision ID: 4f09001b34e6
Revises: 15f941de8d61
Create Date: 2015-05-07 11:04:31.420382

"""

# revision identifiers, used by Alembic.
revision = '4f09001b34e6'
down_revision = '15f941de8d61'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


def upgrade():
    # Move the data over
    engine = op.get_bind().engine
    query = "SELECT DISTINCT pkg_name FROM files"
    results = engine.execute(text(query))
    bquery = "INSERT INTO packages (pkg_name) VALUES "
    action = bquery + ", ".join(["('%s')" % row[0] for row in results])
    engine.execute(text(action))

    engine = op.get_bind().engine
    query = "SELECT DISTINCT pkg_name, tarball, tar_sum FROM files"
    results = engine.execute(text(query))
    bquery = "INSERT INTO releases (pkg_name, tarball, tar_sum) VALUES "
    action = bquery + ", ".join([
        "('%s', '%s', '%s')" % (row[0], row[1], row[2]) for row in results])
    engine.execute(text(action))

def downgrade():
    pass
