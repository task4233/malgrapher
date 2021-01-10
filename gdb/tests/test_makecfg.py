import unittest
from makecfg.config import Config
from makecfg.makecfg import MakeCFG

class TestMakeCFG(unittest.TestCase):
    """test methods for MakeCFG class
    """

    def setUp(self):
        target_file_path = './target/test'
        self.config = Config(target_file_path)
        self.makecfg = MakeCFG(target_file_path)
    
    def test_create_breakpoint(self):
        """test method for create_breakpoint
        """

        got = self.makecfg.create_breakpoint()
        want = ['0x0000555555554654',
              '0x0000555555554666',
              '0x0000555555554674',
              '0x0000555555554682',
              '0x0000555555554694',
              '0x00005555555546a2']
        self.assertCountEqual(want, got)
        self.assertListEqual(want, got)
        