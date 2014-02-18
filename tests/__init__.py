#!/usr/bin/env python

'''
Unit-tests.
'''

import unittest
import shutil
import sys
import os

from datetime import date
from datetime import timedelta

sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..'))

import summershum.utils


class UtilsTest(unittest.TestCase):
    """ summershum.utils tests. """

    # pylint: disable=C0103
    def setUp(self):
        """ Set up the environnment, ran before every tests. """
        if os.path.exists('root'):
            shutil.rmtree('root')

    def test_walk_directory(self):
        """ Test the walk_directory function. """
        # Create directory structure
        os.makedirs('root/fold1/fold2/fold3')
        os.makedirs('root/fold1/fold2/fold4')
        os.makedirs('root/fold1/fold2.5')

        # Write the files
        open('root/file1', 'w').close()
        open('root/fold1/file2', 'w').close()
        open('root/fold1/file3', 'w').close()
        open('root/fold1/fold2/file4', 'w').close()
        open('root/fold1/fold2/fold3/file5', 'w').close()
        open('root/fold1/fold2/fold4/file6', 'w').close()
        open('root/fold1/fold2.5/file6', 'w').close()

        s1 = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
        s2 = 'da39a3ee5e6b4b0d3255bfef95601890afd80709'
        s3 = 'd41d8cd98f00b204e9800998ecf8427e'
        exp_list = [
            ('root/file1', s1, s2, s3),
            ('root/fold1/file2', s1, s2, s3),
            ('root/fold1/file3', s1, s2, s3),
            ('root/fold1/fold2.5/file6', s1, s2, s3),
            ('root/fold1/fold2/file4', s1, s2, s3),
            ('root/fold1/fold2/fold3/file5', s1, s2, s3),
            ('root/fold1/fold2/fold4/file6', s1, s2, s3),
        ]

        # Walk the directory structure
        obs_list = sorted(list(summershum.utils.walk_directory('root')))

        self.assertEqual(exp_list, obs_list)

        # Delete the directory structure
        shutil.rmtree('root')


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(UtilsTest)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
