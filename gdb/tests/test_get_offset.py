import unittest
from makecfg import get_offset

class TestGetOffset(unittest.TestCase):
    """test methods for get_offset.py
    """

    def setUp(self):
        self.target_file_path = 'target/test32'

    def test_get_offset(self):
        """test method for get_offset
        """
        got = get_offset(self.target_file_path)
        want = '0x555555554000'
        self.assertEqual(got, want)