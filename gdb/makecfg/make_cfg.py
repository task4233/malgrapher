import subprocess
import os
from makecfg.config import Config

class Register:
    def __init__(self, register_file_path):
        self.regs = {}
        outs = []
        with open(register_file_path, 'r') as f:
            outs = f.readlines()
        for reg in outs:
            tmp = reg.split(' ')
            tmp = [t for t in tmp if t != '']
            # regs[name] = value
            # regs['rax'] = 0x55555555463a
            self.regs[tmp[0]] = tmp[1]

class MakeCFG:
    def __init__(self, target_file_path):
        self.target_file_path = target_file_path
        self.config = Config(self.target_file_path)
        self.make_breakpoints_file_path = "./gdb_scripts/make_breakpoints.py"
        self.get_registers_file_path = "./gdb_scripts/get_registers.py"
        self.make_cfg_file_path = "./gdb_scripts/make_cfg.py"

    def create_breakpoints(self):
        # あまり良くないけどファイルで渡す
        with open('breakpoint_addrs.dat', 'w') as f:
            addrs = self.config.get_jmp_runtime_addrs()
            addrs.extend(self.config.get_ret_runtime_addrs())
            for addr in addrs:
                f.write(addr + '\n')
        
        with open(os.devnull, 'w') as nu:
            init_args = ['rm', '-f', 'tmp_create_breakpoints.out']
            subprocess.call(init_args, stdout=nu)

            gdb_args = ['gdb', '-q', '-x', self.make_breakpoints_file_path, self.target_file_path]
            subprocess.call(gdb_args, stdout=nu)

        cat_args = ['cat', 'tmp_create_breakpoints.out']
        proc1 = self.__subprocess_helper(cat_args)

        filter_awk_args = ['awk', '{print $5}']
        proc2 = self.__subprocess_helper(filter_awk_args, _stdin=proc1.stdout)
        proc1.stdout.close()

        res = proc2.communicate()[0].decode('utf8').split('\n')
        # 先頭は空
        return res[1:-1]
    
    def make_cfg(self):
        with open(os.devnull, 'w') as nu:
            init_args = ['rm', '-f', 'tmp_make_cfg.out']
            subprocess.call(init_args, stdout=nu)
            
            gdb_args = ['gdb', '-q', '-x', self.make_cfg_file_path, self.target_file_path]
            subprocess.call(gdb_args)
        return None

    def get_registers(self):
        with open(os.devnull, 'w') as nu:
            init_args = ['rm', '-f', 'tmp_get_registers.out']
            subprocess.call(init_args, stdout=nu)

            gdb_args = ['gdb', '-q', '-x', self.get_registers_file_path, self.target_file_path]
            subprocess.call(gdb_args, stdout=nu)
            
        reg = Register('tmp_get_registers.out')
        return reg.regs
    
    def __subprocess_helper(self, args, _stdin=None, _stdout=subprocess.PIPE):
        return subprocess.Popen(args, stdin=_stdin, stdout=_stdout)