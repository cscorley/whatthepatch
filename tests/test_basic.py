# -*- coding: utf-8 -*-
# test_basic.py

from context import whatthepatch

import unittest
from io import StringIO

class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_truth(self):
        assert True
        assert not False

if __name__ == '__main__':
    unittest.main()
