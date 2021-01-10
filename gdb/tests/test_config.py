import unittest
import sys
from makecfg.config import Config


class TestConfig(unittest.TestCase):
    """test methods for Config class
    """

    def setUp(self):
        target_file_path = './target/test'
        self.config = Config(target_file_path)

    def test_environ(self):
        """test environ ENV is test
        """

        got = self.config.ENV
        want = 'test'
        self.assertEqual(got, want)

    def test_get_ret_addrs(self):
        """test method for get_ret_addrs
        """

        got = self.config.get_ret_addrs()
        want = ['0x4fe', '0x591', '0x5e1', '0x620', '0x628', '0x6b6', '0x724', '0x730', '0x73c']
        self.assertCountEqual(want, got)
        self.assertListEqual(want, got)

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
        want = ['0x555555554654', '0x555555554666', '0x555555554674',
                '0x555555554682', '0x555555554694', '0x5555555546a2']
        self.assertCountEqual(want, got)
        self.assertListEqual(want, got)

    def test_get_ret_runtime_addrs(self):
        """test method for get_ret_runtime_addrs
        """

        got = self.config.get_ret_runtime_addrs()
        want = ['0x5555555544fe', '0x555555554591', '0x5555555545e1', '0x555555554620',
                '0x555555554628', '0x5555555546b6', '0x555555554724', '0x555555554730', '0x55555555473c']
        self.assertCountEqual(want, got)
        self.assertListEqual(want, got)


if __name__ == '__main__':
    unittest.main()
