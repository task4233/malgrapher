import gdb
import unittest
from .cfg import CFG


class TestCFG(unittest.TestCase):
    def setUp(self):
        """ mainはif文が3つある実行ファイル
        // bb0
        int flg=0, flg2=1;
        if (flg)
            // bb1
            if (flg2)
                // bb2
                puts("tt");
            else
                // bb3
                puts("tf");
        else
            // bb4
            if (flg2)
                // bb5
                puts("ft");
            else
                // bb6
                puts("ff");
        // bb7
        """
        target = "./target/main"
        self.cfg = CFG(target)
        pass

    def tearDown(self):
        del self.cfg
        pass

    def testCFG(self):
        actual = self.cfg.gen()
        # このwantは一例
        want = [[1,2],[3,4],[5,6],[7],[7],[7],[7],[]]
        for pair in zip(actual, want):
            self.assertEqual(pair[0], pair[1])
        pass
