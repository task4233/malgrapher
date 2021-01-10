import gdb

# from make_breakpoints.py
def create_breakpoints():
    addrs = []
    with open('breakpoint_addrs.dat', 'r') as f:
        addrs = f.readlines()
    for addr in addrs:
        gdb.execute('b *' + addr)

# from make_cfg.py
class Register:
    def __init__(self, regs):
        self.regs = {}
        outs = regs.split('\n')
        for reg in outs:
            tmp = reg.split(' ')
            tmp = [t for t in tmp if t != '']
            # regs[name] = value
            # regs['rax'] = 0x55555555463a
            self.regs[tmp[0]] = tmp[1]

# from get_registers.py
def get_registers():
    """ get_registers get register at that time and return values
    """
    regs = gdb.execute('info registers', to_string=True)
    return Register(regs)

class GDBMgr:
    """ GDBMgr manages the output from gdb
    """
    def __init__(self, line):
        # => 0x55555555463e <main+4>:     sub    rsp,0x10
        tmp = line.split(' ')
        tmp = [t for t in tmp if t != '']
        # tmp:  ['=>', '0x555555554694', '<main+90>:\tje', '0x5555555546a4', '<main+106>\n']
        print("tmp", tmp)
        self.current_addr = tmp[1]
        self.opcode = tmp[2][tmp[2].rfind('\t')+1:]
        self.args = tmp[3:]
        self.raw = line


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
    gdb.execute('info breakpoints')

    while True:
        gdb.execute('n')
        # => 0x55555555463e <main+4>:     sub    rsp,0x10
        info = GDBMgr(gdb.execute('x/i $pc', to_string=True))
        
        if 'ret' in info.opcode:
            break

        # jmp系命令の時
        if 'j' in info.opcode:
            cfg.append(CFG())
    
    gdb.execute('quit')

make_cfg()