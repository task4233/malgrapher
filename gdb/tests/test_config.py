import unittest
import sys, os
from makecfg.config import Config


class TestConfig(unittest.TestCase):
    """test methods for Config class
    """

    def setUp(self):
        self.target_file_path = 'target/test32'
        self.config = Config(self.target_file_path)

    def test_environ(self):
        """test environ ENV is test
        """

        got = self.config.ENV
        want = 'test'
        self.assertEqual(got, want)
    
    def test_target(self):
        """test environ TARGET_FILE
        """

        got = self.target_file_path
        want = 'target/test32'
        self.assertEqual(got, want)


if __name__ == '__main__':
    unittest.main()
