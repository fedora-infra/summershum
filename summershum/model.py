import datetime
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

BASE = declarative_base()


def create_session(db_url, alembic_ini=None, debug=False, create=False):
    """ Create the tables in the database using the information from the
    url obtained.

    :arg db_url, URL used to connect to the database. The URL contains
        information with regards to the database engine, the host to
        connect to, the user and password and the database name.
          ie: <engine>://<user>:<password>@<host>/<dbname>
    :kwarg alembic_ini, path to the alembic ini file. This is necessary
        to be able to use alembic correctly, but not for the unit-tests.
    :kwarg debug, a boolean specifying wether we should have the verbose
        output of sqlalchemy or not.
    :return a session that can be used to query the database.

    """
    engine = create_engine(db_url, echo=debug)

    if create:
        BASE.metadata.create_all(engine)

    if alembic_ini is not None:  # pragma: no cover
        # then, load the Alembic configuration and generate the
        # version table, "stamping" it with the most recent rev:
        from alembic.config import Config
        from alembic import command
        alembic_cfg = Config(alembic_ini)
        command.stamp(alembic_cfg, "head")

    scopedsession = scoped_session(sessionmaker(bind=engine))
    return scopedsession


class Package(BASE):
    """ The ``packages`` table in the database containing all the sha1sum
    of all the files in all the packages.
    """
    __tablename__ = 'packages'

    id = sa.Column(sa.Integer, primary_key=True)
    pkg_name = sa.Column(sa.String(200), index=True, nullable=False)
    filename = sa.Column(sa.String(200), nullable=False)
    sha1sum = sa.Column(sa.String(200), index=True, nullable=True)
    version = sa.Column(sa.String(50), nullable=False)
    created_on = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (
        sa.UniqueConstraint('pkg_name', 'filename', 'version'),
    )

    def __repr__(self):
        """ String representation of that object. """
        return '<Package(project:%s, file:%s, sha1:%s)>' % (
            self.pkg_name, self.filename, self.sha1sum)

    @classmethod
    def by_sha(cls, session, sha1sum):
        """ Retrieve the packages having the specified sha1sum. """
        query = session.query(
            cls
        ).filter(
            cls.sha1sum == sha1sum
        )

        return query.all()

    @classmethod
    def exists(cls, session, pkg_name, filename, version):
        """ Retrieve the packages having the specified package name,
        filename and version.
        """
        query = session.query(
            cls
        ).filter(
            cls.pkg_name == pkg_name
        ).filter(
            cls.filename == filename
        ).filter(
            cls.version == version
        ).order_by(
            cls.filename, cls.version
        )

        return query.first()

    get = exists
