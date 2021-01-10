import gdb
from make_breakpoints import create_breakpoints

class GDBMgr:
    """ GDBMgr manages the output from gdb
    """
    def __init__(self, line):
        tmp = line.split(' ')
        self.current_addr = tmp[1]
        self.opcode = tmp[3]
        self.dst = tmp[4]
        self.frm = tmp[5]


class CFG:
    """ CFG manages node of CFG
    """
    def __init__(self):
        self.lb_addr = "" # lower bound
        self.ub_addr = "" # upper bound
        self.dsts = []
        pass


def make_cfg():
    cfg = []
    create_breakpoints()
    
    # 実行
    gdb.execute('run')

    while True:
        gdb.execute('next')
        # => 0x55555555463e <main+4>:     sub    rsp,0x10
        info = GDBMgr(gdb.execute('x/i $pc', to_string=True))
        
        # jmp系命令の時
        if 'j' in info.opcode:
            cfg.append(CFG())

make_cfg()