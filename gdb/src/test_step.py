import unittest
from .step import Breakpoint

class TestBreakpoint(unittest.TestCase):
    def setUp(self):
        print("setup")
        # => 0x555555554694 <main+90>:	je     0x5555555546a4 <main+106>
        self.line = "=> 0x555555554694 <main+90>:	je     0x5555555546a4 <main+106>"
        self.bp = Breakpoint(self.line)

    def tearDown(self):
        print("tearDown")
        del self.line
        del self.bp

    def test_split_output(self):
        """ test constructor for Breakpoint """
        words = self.line.split()
        self.assertEqual(self.bp.from_addr, words[1])
        self.assertEqual(self.bp.op, words[3])
        self.assertEqual(self.bp.args, words[4:])

if __name__ == '__main__':
    unittest.main()
