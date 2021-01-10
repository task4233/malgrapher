import gdb
from collections import deque

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
            if len(tmp) < 2:
                continue
            self.regs[tmp[0]] = tmp[1]

# from get_registers.py
def get_registers():
    """ get_registers get register at that time and return values
    """
    regs = gdb.execute('info registers', to_string=True)
    return Register(regs)

def restore_registers(regs):
    """ restore_registers restore register with register information
    """
    print(regs.regs)
    for name, value in regs.regs.items():
        gdb.execute('set $' + name + '=' + value)
    return get_registers()

class GDBMgr:
    """ GDBMgr manages the output from gdb
    """
    def __init__(self, lines, regs=None):
        # => 0x55555555463e <main+4>:     sub    rsp,0x10
        tmp = (lines[0]).split(' ')
        tmp = [t for t in tmp if t != '']
        # tmp:  ['0x555555554694', '<main+90>:\tje', '0x5555555546a4', '<main+106>\n']
        self.addr = tmp[0]
        self.opcode = tmp[1][tmp[1].rfind('\t')+1:]
        self.args = tmp[1:]
        self.raw = lines[1]

        tmp = lines[1].split(' ')
        tmp = [t for t in tmp if t != '']
        self.naddr = tmp[0]
        self.nopcode = tmp[1][tmp[1].rfind('\t')+1:]
        self.nargs = tmp[1:]
        self.nraw = lines[1]

class CFG:
    """ CFG manages node of CFG
    """
    def __init__(self):
        self.lb_addr = "" # lower bound
        self.ub_addr = "" # upper bound
        self.dsts = []
        pass

def andf(f1, f2):
    return f1 + "&" + f2

def notf(flag):
    return "!(" + flag + ")"

def update_eflags(opcode, status):
    if opcode == "jmp":
        return

    operation = 'set $eflags'
    flag = {
        "CF": "1 << 0",
        "PF": "1 << 2",
        "ZF": "1 << 6",
        "SF": "1 << 7",
    }

    true_stat = {
        # "opcode": "trueの時の条件"
        "je": flag["ZF"],
        "jne": notf(flag["ZF"]),
        "ja": andf(notf(flag["CF"]), notf(flag["ZF"])),
    }

    if status:
        # フラグを立てる
        operation += ' |= (' + true_stat[opcode] + ')'
    else:
        # フラグを倒す
        operation += ' &= (' + true_stat[opcode] + ')'
    gdb.execute(operation)

def make_cfg():
    cfg = []
    create_breakpoints()
    ub_addr = "0x0"
    deq = deque([])

    # 実行
    gdb.execute('run')
    gdb.execute('info breakpoints')

    while True:
        gdb.execute('n')
        # => 0x55555555463e <main+4>:     sub    rsp,0x10
        lines = gdb.execute('x/2i $rip', to_string=True).split('\n')
        lines[0] = lines[0][3:] # delete => 
        info = GDBMgr(lines, get_registers())
        if 'ret' in info.nopcode:
            if len(deq) > 0:
                restore = deq.pop()
                restore_registers(restore.regs)
                print("restore: " + restore.raw)
                gdb.execute("jmp *" + restore.addr)
                continue
            gdb.execute('info breakpoints')
            break

        # jmp系命令の時
        if 'j' in info.opcode:
            # print(info.raw)
            cfg.append(CFG())

            # 次に呼ばれる時はfalseなので, 設定してからstackに積む
            update_eflags(info.opcode, True)
            info.regs = get_registers()
            deq.append(info)

            # trueに変更
            update_eflags(info.opcode, False)
    gdb.execute('quit')

make_cfg()