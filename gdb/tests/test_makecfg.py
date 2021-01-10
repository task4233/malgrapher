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
        want = ['0x0000555555554654', '0x0000555555554666', '0x0000555555554674', '0x0000555555554682', '0x0000555555554694', '0x00005555555546a2', '0x00005555555544fe',
                '0x0000555555554591', '0x00005555555545e1', '0x0000555555554620', '0x0000555555554628', '0x00005555555546b6', '0x0000555555554724', '0x0000555555554730', '0x000055555555473c']
        self.assertCountEqual(want, got)
        self.assertListEqual(want, got)

    def test_get_registers(self):
        """test method for get_registers
        """

        got = self.makecfg.get_registers()
        want = {'rax': '0x55555555463a',
                'rbx': '0x0',
                'rcx': '0x5555555546c0',
                'rdx': '0x7fffffffe058',
                'rsi': '0x7fffffffe048',
                'rdi': '0x1',
                'rbp': '0x7fffffffdf60',
                'rsp': '0x7fffffffdf60',
                'r8': '0x7ffff7dced80',
                'r9': '0x7ffff7dced80',
                'r10': '0x0',
                'r11': '0x0',
                'r12': '0x555555554530',
                'r13': '0x7fffffffe040',
                'r14': '0x0',
                'r15': '0x0',
                'rip': '0x55555555463e',
                'eflags': '0x246',
                'cs': '0x33',
                'ss': '0x2b',
                'ds': '0x0',
                'es': '0x0',
                'fs': '0x0',
                'gs': '0x0'}
        self.assertDictEqual(got, want)

    def test_make_cfg(self):
        """test method make_cfg
        """
        got = self.makecfg.make_cfg()
        want = None
        self.assertEqual(want, got)
