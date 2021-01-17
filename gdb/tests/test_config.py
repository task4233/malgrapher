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

    def test_get_func_addrs(self):
        """test method for get_func_addrs
        """

        func_name = 'main'
        got = self.config.get_func_addrs(func_name)
        want = ['0x63a', '0x63b', '0x63e', '0x642', '0x649', '0x650', '0x654', '0x656', '0x65d', '0x662', '0x666', '0x668', '0x66f', '0x674',
                '0x676', '0x67d', '0x682', '0x684', '0x68b', '0x690', '0x694', '0x696', '0x69d', '0x6a2', '0x6a4', '0x6ab', '0x6b0', '0x6b5', '0x6b6']
        self.assertCountEqual(want, got)
        self.assertListEqual(want, got)

    def test_get_ret_addrs(self):
        """test method for get_ret_addrs
        """

        got = self.config.get_ret_addrs()
        want = ['0x4fe', '0x591', '0x5e1', '0x620',
                '0x628', '0x6b6', '0x724', '0x730', '0x73c']
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

    def test_get_func_runtime_addrs(self):
        """test method for get_func_runtime_addrs
        """

        func_name = 'main'
        got = self.config.get_func_runtime_addrs(func_name)
        want = ['0x55555555463a', '0x55555555463b', '0x55555555463e', '0x555555554642', '0x555555554649', '0x555555554650', '0x555555554654', '0x555555554656', '0x55555555465d', '0x555555554662', '0x555555554666', '0x555555554668', '0x55555555466f', '0x555555554674',
                '0x555555554676', '0x55555555467d', '0x555555554682', '0x555555554684', '0x55555555468b', '0x555555554690', '0x555555554694', '0x555555554696', '0x55555555469d', '0x5555555546a2', '0x5555555546a4', '0x5555555546ab', '0x5555555546b0', '0x5555555546b5', '0x5555555546b6']
        self.assertCountEqual(want, got)
        self.assertListEqual(want, got)

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
