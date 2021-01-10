import unittest
from makecfg.config import Config

class TestConfig(unittest.TestCase):
    """test methods for Config class
    """
    def setUp(self):
        target_file_path = './target/test'
        self.config = Config(target_file_path)

    def test_get_jmp_addrs(self):
        """test method for get_jmp_addrs
        """

        got = self.config.get_jmp_addrs()
        want = ['0x654', '0x666', '0x674', '0x682', '0x694', '0x6a2']
        self.assertCountEqual(want, got)
        self.assertListEqual(want, got)

    def test_get_stop_addr_objdump(self):
        """test method for get_stop_addr_objdump
        """

        got = self.config.get_stop_addr_objdump()
        want = '0x63e'
        self.assertEqual(want, got)

    def test_get_stop_addr_gdb(self):
        """test method for get_stop_addr_gdb
        """

        got = self.config.get_stop_addr_gdb()
        want = '0x55555555463e'
        self.assertEqual(want, got)

    def test_get_offset_with_objdump_and_gdb(self):
        """test method for get_offset_with_objdump_and_gdb
        """

        got = self.config.get_offset_with_objdump_and_gdb()
        want = '0x555555554000'
        self.assertEqual(want, got)

    def test_get_jmp_runtime_addrs(self):
        """test method for get_jmp_runtime_addrs
        """

        got = self.config.get_jmp_runtime_addrs()
        want = ['0x555555554654','0x555555554666','0x555555554674', '0x555555554682', '0x555555554694', '0x5555555546a2']
        self.assertCountEqual(want, got)
        self.assertListEqual(want, got)

if __name__ == '__main__':
    unittest.main()
