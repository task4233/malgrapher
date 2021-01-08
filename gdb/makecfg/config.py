import subprocess

class Config:
    # init
    def __init__(self, target_file_path, get_stop_addr_script_file_path="./gdb_scripts/get_stop_addr.py"):
        self.target_file_path = target_file_path
        self.get_stop_addr_script_file_path = get_stop_addr_script_file_path
    
    # objdumpでjmp系命令を全て取得
    def get_jmp_addrs(self):
        objdump_args = ['objdump', '-d', '-M', 'intel', self.target_file_path]
        proc1 = self.__subprocess_helper(objdump_args)

        filter_jump_args = ['grep', 'j']
        proc2 = self.__subprocess_helper(filter_jump_args, proc1.stdout)
        proc1.stdout.close()

        filter_main_args = ['grep', 'main']
        proc1 = self.__subprocess_helper(filter_main_args, proc2.stdout)
        proc2.stdout.close()

        filter_cut_args = ['cut', '-d', ':', '-f', '1']
        proc2 = self.__subprocess_helper(filter_cut_args, proc1.stdout)
        proc1.stdout.close()

        output = proc2.communicate()[0].decode('utf8')
        jmp_addrs = []
        if '\n' in output:
            jmp_addrs = output.split('\n')[:-1]
            jmp_addrs = [hex(int(addr.strip(' '), 16)) for addr in jmp_addrs]
        return jmp_addrs

    # objdumpでの止まるアドレスを取得
    def get_stop_addr_objdump(self):
        objdump_args = ['objdump', '-d', '-M', 'intel', self.target_file_path]
        proc1 = self.__subprocess_helper(objdump_args)

        filter_main_args = ['grep', '-A', '5', '<main>']
        proc2 = self.__subprocess_helper(filter_main_args, proc1.stdout)
        proc1.stdout.close()

        filter_stop_addr = ['grep', 'sub']
        proc1 = self.__subprocess_helper(filter_stop_addr, proc2.stdout)
        proc2.stdout.close()

        filter_cut_args = ['cut', '-d', ':', '-f', '1']
        proc2 = self.__subprocess_helper(filter_cut_args, proc1.stdout)
        proc1.stdout.close()

        output = hex(int(proc2.communicate()[0].decode('utf8').strip(' '), 16))
        return output

    # gdb実行時での止まるアドレスを取得
    def get_stop_addr_gdb(self):
        init_args = ['rm', 'tmp.out']
        subprocess.call(init_args)

        gdb_args = ['gdb', '-q', '-x', self.get_stop_addr_script_file_path, self.target_file_path]
        subprocess.call(gdb_args)

        filter_cat_args = ['cut', '-d', ' ', '-f', '2', 'tmp.out']
        addr = subprocess.check_output(filter_cat_args)
        return addr.decode('utf8').strip('\n')

    # objdumpとgdb実行時のoffsetを取得
    def get_offset_with_objdump_and_gdb(self):
        return hex(int(self.get_stop_addr_gdb(), 0) - int(self.get_stop_addr_objdump(), 0))

    # breakpointを立てるアドレスを再計算(offsetを考慮する)
    def get_jmp_runtime_addrs(self):
        offset = self.get_offset_with_objdump_and_gdb()
        addrs = self.get_jmp_addrs()
        addrs = [hex(int(addr, 0) + int(offset, 0)) for addr in addrs]
        return addrs

    def __subprocess_helper(self, args, _stdin=None, _stdout=subprocess.PIPE):
        return subprocess.Popen(args, stdin=_stdin, stdout=_stdout)
