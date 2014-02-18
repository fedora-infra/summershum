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


class File(BASE):
    """ The ``files`` table in the database containing all the sha256sum
    of all the files in all the packages.
    """
    __tablename__ = 'files'

    id = sa.Column(sa.Integer, primary_key=True)
    filename = sa.Column(sa.Text, nullable=False)

    # This is our primary means of distinguishing files
    sha256sum = sa.Column(sa.String(64), index=True, nullable=True)
    # We also keep others in the wild case that there's a sha256 collision.
    sha1sum = sa.Column(sa.String(40), index=True, nullable=True)
    md5sum = sa.Column(sa.String(32), index=True, nullable=True)

    pkg_name = sa.Column(sa.Text, index=True, nullable=False)
    tar_file = sa.Column(sa.Text, nullable=False)

    # For now, this is an md5 handed to us by another application, so it need
    # only be 32 bits.  But in the future we'd like to move to a more modern
    # hash.  Therefore we size this column up to 64 bits.
    tar_sum = sa.Column(sa.String(64), index=True, nullable=False)

    created_on = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (
        sa.UniqueConstraint('tar_sum', 'filename'),
    )

    def __repr__(self):
        """ String representation of that object. """
        return '<File(tar_file:%s, filename:%s, sha256:%s)>' % (
            self.tar_file, self.filename, self.sha256sum)

    @classmethod
    def by_sha256(cls, session, sha256sum):
        """ Retrieve the files having the specified sha256sum. """
        query = session.query(cls).filter(cls.sha256sum == sha256sum)
        return query.all()

    @classmethod
    def by_sha1(cls, session, sha1sum):
        """ Retrieve the files having the specified sha1sum. """
        query = session.query(cls).filter(cls.sha1sum == sha1sum)
        return query.all()

    @classmethod
    def by_md5(cls, session, md5sum):
        """ Retrieve the files having the specified md5sum. """
        query = session.query(cls).filter(cls.md5sum == md5sum)
        return query.all()

    @classmethod
    def by_tar_sum(cls, session, tar_sum):
        """ Retrieves all the files having the specified tar_sum
        (the md5sum of the whole tarball)
        """
        query = session.query(cls).filter(cls.tar_sum == tar_sum)
        query = query.order_by(cls.pkg_name, cls.tar_file, cls.filename)

        return query.all()

    @classmethod
    def exists(cls, session, tar_sum, filename):
        """ Retrieve the file that has:

        - a particular tarball md5sum
        - a particular filename
        """
        query = session.query(cls).filter(
            cls.tar_sum == tar_sum
        ).filter(
            cls.filename == filename
        ).order_by(
            cls.pkg_name, cls.tar_file, cls.filename
        )

        return query.first()

    get = exists
