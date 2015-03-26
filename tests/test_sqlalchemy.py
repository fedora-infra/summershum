import unittest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, File

# create in-memory database for test 
class TestQuery(unittest.TestCase):
    # set up the database
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.session = Session(engine)

        Base.metadata.create_all(self.engine)
        self.file = File(
	    filename='/pcre-8.36/makevp_l.txt', 
            sha256sum=adeb5f421a231c3191246501e48f0306506a90fee4cebfe61db4d24e18df81f8, 
	    sha1sum=fac84e09fcf69ae985c81f2f93f72281a693a05a, 
	    md5sum=8891f3a734f71a632c8b43d48e88b336, 
	    pkg_name='mingw-pcre', 
	    tarball=pcre-8.36.tar.bz2, 
	    tar_sum=b767bc9af0c20bc9c1fe403b0d41ad97, 
	    created_on=datetime('2014-12-25 21:49:44.176689')
        self.session.add(self.file)
        self.session.commit()

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_query_file(self):
        expected = [self.file]
        result = self.session.query(File).all()
        expected =  File(
	    filename='/pcre-8.36/makevp_l.txt', 
            sha256sum=adeb5f421a231c3191246501e48f0306506a90fee4cebfe61db4d24e18df81f8, 
	    sha1sum=fac84e09fcf69ae985c81f2f93f72281a693a05a, 
	    md5sum=8891f3a734f71a632c8b43d48e88b336, 
	    pkg_name='mingw-pcre', 
	    tarball=pcre-8.36.tar.bz2, 
	    tar_sum=b767bc9af0c20bc9c1fe403b0d41ad97, 
	    created_on=datetime('2014-12-25 21:49:44.176689')
        self.assertEqual(result, expected)
