import unittest, os
from makecfg.config import Config
from makecfg.make_cfg import MakeCFG


class TestMakeCFG(unittest.TestCase):
    """test methods for MakeCFG class
    """

    def setUp(self):
        target_file_path = 'target/test32'
        self.config = Config(target_file_path)
        self.makecfg = MakeCFG(target_file_path)

