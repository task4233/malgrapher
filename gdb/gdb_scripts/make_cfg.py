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

# from get_registers.py
def get_registers():
    """ get_registers get register at that time and return values
    """
    regs = gdb.execute('info registers', to_string=True)
    return Register(regs)


def restore_registers(regs):
    """ restore_registers restore register with register information
    """
    for name, value in regs.regs.items():
        gdb.execute('set $' + name + '=' + value)
    return get_registers()


class GDBMgr:
    """ GDBMgr manages the output from gdb
    """

    def __init__(self, line, regs=None):
        # => 0x55555555463e <main+4>:     sub    rsp,0x10
        tmp = line.split(' ')
        tmp = [t for t in tmp if t != '']
        # tmp:  ['0x555555554694', '<main+90>:\tje', '0x5555555546a4', '<main+106>\n']
        print("tmp:", tmp)
        self.addr = tmp[0]
        self.opcode = tmp[1][tmp[1].rfind('\t')+1:]
        self.args = tmp[1:]
        self.raw = line
        self.regs = regs

class CFG:
    """ CFG manages node of CFG
    """
    def __init__(self):
        self.nodes = []
    
    def get_idx(self, addr_str):
        for idx, node in self.nodes:
            if int(node.lb_addr, 0) < int(addr_str, 0) and \
                int(addr_str, 0) < int(node.ub_addr, 0):
                return idx
        self.nodes.append(Node()) # ここ少し考えた方が良いかも
        return len(self.nodes)-1 # 最後の要素を返す
    
    def append(self, node):
        self.nodes.append(node)

class Node:
    """Node manages node of CFG
    """
    def __init__(self):
        self.lb_addr = ""  # lower bound
        self.ub_addr = ""  # upper bound
        self.dsts = []
        self.lines = {}

    def set_lines(self, addr_str, info):
        if addr_str in self.lines:
            return
        self.lines[addr_str] = info
    
    def __str__(self):
        return "[%s, %s], dst=%s, lines=%s" % (self.lb_addr, self.ub_addr, ",".join(self.dsts), ",".join(["[{0}, {1}]".format(k, v) for (k,v) in self.lines.items()]))


def make_cfg():
    cfg = CFG()
    node = Node()
    create_breakpoints()
    ub_addr = "0x0"
    stack = []

    # 実行
    gdb.execute('run')
    gdb.execute('info breakpoints')

    while True:
        gdb.execute('n')
        # => 0x55555555463e <main+4>:     sub    rsp,0x10
        lines = gdb.execute('x/2i $rip', to_string=True).split('\n')
        print(lines)
        lines[0] = lines[0][3:]  # delete =>

        lines = [GDBMgr(line) for line in lines if len(line) > 0]
        [node.set_lines(line.addr, line) for line in lines]
        # レジスタ保存
        lines[0].reg = get_registers()

        if 'ret' in lines[1].opcode:
            if len(stack) > 0:
                (restore, status) = stack.pop()
                restore_registers(restore.regs)
                # statusを逆転
                update_eflags(restore.opcode, not(status))
                print("restore: " + restore.raw)
                gdb.execute("jmp *" + restore.addr)
                continue
            gdb.execute('info breakpoints')
            break

        # jmp系命令の時
        if 'j' in lines[1].opcode:
            # print(info.raw)
            node = Node()
            cfg.append(node)

            # 次に呼ばれる時はfalseなので, 設定してからstackに積む
            lines[1].regs = get_registers()
            stack.append((lines[1], True))

            # trueに変更
            update_eflags(lines[1].opcode, True)

            # ジャンプ先の情報を取得
            gdb.execute("n")
            line = gdb.execute('x/i $rip', to_string=True)
            line = GDBMgr(line[3:])

            if int(line.addr, 0) < int(ub_addr, 0):
                # もう到達したところ
                idx = cfg.get_idx(line.addr)
                cfg.nodes[idx].dsts = len(cfg.nodes)-1 # 末尾がdst idx
            else:
                # まだ到達していないところ
                ub_addr = line.addr
            # メモリをrestoreしてtopの情報を復元
            restore_registers(lines[1].regs)
            update_eflags(lines[1].opcode, False)
            gdb.execute("jmp *" + lines[1].addr)

    for node in cfg.nodes:
        print(node)
    gdb.execute('quit')


make_cfg()
