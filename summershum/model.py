import datetime
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation
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
    """ The ``packages`` table stores the name of the different packages
    for which we store file name/hash.
    """
    __tablename__ = 'packages'

    pkg_name = sa.Column(sa.Text, primary_key=True)


class Release(BASE):
    """ The ``releases`` table stores for each package the releases that have
    been covered by summershum.
    """
    __tablename__ = 'releases'

    pkg_name = sa.Column(
        sa.Text,
        sa.ForeignKey('packages.pkg_name', onupdate='CASCADE'),
        nullable=False,
        index=True)

    tarball = sa.Column(sa.Text, primary_key=True)

    # For now, this is an md5 handed to us by another application, so it need
    # only be 32 bits.  But in the future we'd like to move to a more modern
    # hash.  Therefore we size this column up to 64 bits.
    tar_sum = sa.Column(sa.String(64), primary_key=True)

    package = relation('Package', remote_side=[pkg_name], backref='releases')

    __table_args__ = (
        sa.UniqueConstraint('tarball', 'tar_sum'),
    )

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

    created_on = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)

    tarball = sa.Column(
        sa.Text,
        sa.ForeignKey('releases.tarball', onupdate='CASCADE'),
        nullable=False,
        index=True)

    release = relation('Release', remote_side=[tarball], backref='files')

    __table_args__ = (
        sa.UniqueConstraint('tarball', 'filename'),
    )

    def __repr__(self):
        """ String representation of that object. """
        return '<File(tarball:%s, filename:%s, sha256:%s)>' % (
            self.tarball, self.filename, self.sha256sum)

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
        query = query.order_by(cls.pkg_name, cls.tarball, cls.filename)

        return query.all()

    @classmethod
    def by_package(cls, session, pkg_name):
        """ Retrieve the files having the specified package name. """
        query = session.query(cls).filter(cls.pkg_name == pkg_name)

        return query.all()

    @classmethod
    def by_tarball(cls, session, tarball):
        """ Retrieve the files having the specified tarball. """
        query = session.query(cls).filter(cls.tarball == tarball)

        return query.all()

    @classmethod
    def package_filenames(cls, session, pkg_name):
        """ Retrieve all the files of a package """
        query = session.query(cls.filename).filter(cls.pkg_name == pkg_name)

        return query.all()

    @classmethod
    def by_filename(cls, session, filename):
        """ Retrieve the files having the specified tarball. """
        query = session.query(cls).filter(cls.filename == filename)

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
            cls.pkg_name, cls.tarball, cls.filename
        )

        return query.first()

    get = exists

    @classmethod
    def get_all_packages(cls, session, pattern, extension=None,
                         limit=None, count=False, page=None):
        """ Returns a list of all packages """

        if '*' in pattern:
            pattern = pattern.replace('*', '%')

        if limit is not None:
            try:
                limit = abs(int(limit))
            except ValueError:
                raise PkgdbException('Wrong limit provided')

        if page is not None:
            try:
                page = abs(int(page))
            except ValueError:
                raise PkgdbException('Wrong page provided')

        if page is not None and page > 0 and limit is not None and limit > 0:
            page = (page - 1) * limit

        query = session.query(
            sa.func.distinct(cls.pkg_name)
        ).filter(
            cls.pkg_name.like(pattern)
        ).order_by(
            cls.pkg_name
        )

        if extension:
            query = query.filter(cls.filename.endswith(extension))

        offset = page

        if count:
            return query.count()

        if limit:
            query = query.limit(limit)

        if offset:
            query = query.offset(offset)

        return query.all()

