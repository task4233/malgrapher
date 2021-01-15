import unittest
from makecfg.config import Config
from makecfg.make_cfg import MakeCFG


class TestMakeCFG(unittest.TestCase):
    """test methods for MakeCFG class
    """

    def setUp(self):
        target_file_path = './target/test'
        self.config = Config(target_file_path)
        self.makecfg = MakeCFG(target_file_path)

    def test_create_breakpoints(self):
        """test method for create_breakpoints
        """

        got = self.makecfg.create_breakpoints()
        want = ['0x000055555555463a', '0x000055555555463b', '0x000055555555463e', '0x0000555555554642', '0x0000555555554649', '0x0000555555554650', '0x0000555555554654', '0x0000555555554656', '0x000055555555465d', '0x0000555555554662', '0x0000555555554666', '0x0000555555554668', '0x000055555555466f', '0x0000555555554674',
                '0x0000555555554676', '0x000055555555467d', '0x0000555555554682', '0x0000555555554684', '0x000055555555468b', '0x0000555555554690', '0x0000555555554694', '0x0000555555554696', '0x000055555555469d', '0x00005555555546a2', '0x00005555555546a4', '0x00005555555546ab', '0x00005555555546b0', '0x00005555555546b5', '0x00005555555546b6']
        self.assertCountEqual(want, got)
        self.assertListEqual(want, got)

    def test_get_registers(self):
        """test method for get_registers
        """

        got = self.makecfg.get_registers()
        want = {'rax': '0x55555555463a', 'rbx': '0x0', 'rcx': '0x5555555546c0', 'rdx': '0x7fffffffe048', 'rsi': '0x7fffffffe038', 'rdi': '0x1', 'rbp': '0x7fffffffdf50', 'rsp': '0x7fffffffdf50', 'r8': '0x7ffff7dced80', 'r9': '0x7ffff7dced80',
                'r10': '0x0', 'r11': '0x0', 'r12': '0x555555554530', 'r13': '0x7fffffffe030', 'r14': '0x0', 'r15': '0x0', 'rip': '0x55555555463e', 'eflags': '0x246', 'cs': '0x33', 'ss': '0x2b', 'ds': '0x0', 'es': '0x0', 'fs': '0x0', 'gs': '0x0'}
        self.assertDictEqual(got, want)

    def test_make_cfg(self):
        """test method make_cfg
        """
        got = self.makecfg.make_cfg()
        want = None
        self.assertEqual(want, got)
        pass
