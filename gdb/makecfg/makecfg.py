import subprocess
import os
from makecfg.config import Config

class MakeCFG:
    def __init__(self, target_file_path):
        self.target_file_path = target_file_path
        self.config = Config(self.target_file_path)
        self.make_breakpoints_file_path = "./gdb_scripts/make_breakpoints.py"

    def create_breakpoint(self):
        # あまり良くないけどファイルで渡す
        with open('breakpoint_addrs.dat', 'w') as f:
            addrs = self.config.get_jmp_runtime_addrs()
            for addr in addrs:
                f.write(addr + '\n')
        
        with open(os.devnull, 'w') as nu:
            init_args = ['rm', '-f', 'tmp.out']
            subprocess.call(init_args, stdout=nu)

            gdb_args = ['gdb', '-q', '-x', self.make_breakpoints_file_path, self.target_file_path]
            subprocess.call(gdb_args, stdout=nu)
            
        filter_cut_args = ['cut', '-d', ' ', '-f', '17', 'tmp.out']
        addrs = subprocess.check_output(filter_cut_args)
        res = addrs.decode('utf8').split('\n')
        return res[1:-1]
