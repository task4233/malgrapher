import gdb
import sys
import subprocess
import os

# objdumpでの止まるアドレスを取得
def get_stop_addr_objdump():
    objdump_args = ['objdump', '-d', '-M', 'intel', os.environ['TARGET_FILE']]
    proc1 = __subprocess_helper(objdump_args)

    filter_main_args = ['grep', '-A', '30', '<main>']
    proc2 = __subprocess_helper(filter_main_args, proc1.stdout)
    proc1.stdout.close()

    filter_stop_addr = ['grep', 'sub']
    proc1 = __subprocess_helper(filter_stop_addr, proc2.stdout)
    proc2.stdout.close()

    filter_cut_args = ['cut', '-d', ':', '-f', '1']
    proc2 = __subprocess_helper(filter_cut_args, proc1.stdout)
    proc1.stdout.close()

    output = hex(int(proc2.communicate()[0].decode('utf8').strip(' ').split('\n')[0], 16))
    return output

# objdumpとgdb実行時のoffsetを取得
def get_offset_with_objdump_and_gdb(stop_addr):
    return hex(int(stop_addr, 0) - int(get_stop_addr_objdump(), 0))

def get_func_addrs(func_name):
    gdb_args = ['gdb', '-batch', '-ex', 'file ' + os.environ['TARGET_FILE'], '-ex', 'disassemble ' + func_name]
    proc1 = __subprocess_helper(gdb_args)

    filter_awk_args = ['awk', '{print $1}']
    proc2 = __subprocess_helper(filter_awk_args, proc1.stdout)
    proc1.stdout.close()

    output = proc2.communicate()[0].decode('utf8')
    ret_addrs = []
    if '\n' in output:
        ret_addrs = output.split('\n')[1:-2]
        ret_addrs = [hex(int(addr.strip(' '), 16)) for addr in ret_addrs]
    return ret_addrs

# breakpointを立てるアドレスを再計算
def get_func_runtime_addrs(offset, func_name):
    addrs = get_func_addrs(func_name)
    addrs = [hex(int(addr, 0) + int(offset, 0)) for addr in addrs]
    return addrs  

def __subprocess_helper(args, _stdin=None, _stdout=subprocess.PIPE):
    return subprocess.Popen(args, stdin=_stdin, stdout=_stdout)


# from make_breakpoints.py
def create_breakpoints(stop_addr):
    offset = get_offset_with_objdump_and_gdb(stop_addr)
    func_name = 'main'
    addrs = get_func_runtime_addrs(offset, func_name)
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
            self.regs[tmp[0]] = tmp[1].split('\t')[0]

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
        operation += ' &= !(' + true_stat[opcode] + ')'
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
        # # print("tmp:", tmp)
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
    
    # 引数のaddr_strがどのノード番号に該当するかを返す
    def get_idx(self, addr_str):
        # print(addr_str)
        for idx in range(len(self.nodes)):
            n = self.nodes[idx]
            # print("[", n.lb_addr, n.ub_addr, "]")
            # 満たしたい条件は
            # n.lb_addr <= addr_str && addr_str <= n.ub_addr
            if int(n.lb_addr, 0) > int(addr_str, 0):
                continue
            elif n.ub_addr == "0x0":
                if int(addr_str, 0) != int(n.lb_addr, 0):
                    continue
            elif int(addr_str, 0) > int(n.ub_addr, 0):
                continue
            return idx
        # self.nodes.append(Node()) # ここ少し考えた方が良いかも
        return -1 # 最後の要素を返す
    
    def append(self, node):
        """ append できる条件は, 追加するノードが既知のノードに内包されないこと
        """
        for n in self.nodes:
            if n.lb_addr == node.lb_addr:
                if node.ub_addr > n.ub_addr:
                    n.ub_addr = node.ub_addr
                return
            if int(n.lb_addr, 0) <= int(node.lb_addr, 0) and \
                int(node.ub_addr, 0) <= int(n.ub_addr, 0):
                continue
        self.nodes.append(node)
    
    def append_dst_node(self, frm_addr, dst_addr):
        """ node.dstsにジャンプ先のブロック番号を追加する
        """
        frm_idx = self.get_idx(frm_addr)
        dst_idx = self.get_idx(dst_addr)
        # print("frm: " + frm_addr + ", dst: " + dst_addr)
        # print("frm: " + str(frm_idx) + ", dst: " + str(dst_idx))
        for dst in self.nodes[frm_idx].dsts:
            if dst == dst_idx:
                return
        self.nodes[frm_idx].dsts.append(dst_idx)

class Node:
    """Node manages node of CFG
    """
    def __init__(self):
        self.lb_addr = "0xffffffffffffffff"  # lower bound
        self.ub_addr = "0x0"  # upper bound
        self.dsts = []
    
    # def __str__(self):
    #     return "[%s, %s], dst=%s, lines=%s" % (self.lb_addr, self.ub_addr, ",".join(self.dsts), ",".join(["[{0}, {1}]".format(k, v) for (k,v) in self.lines.items()]))

def print_nodes(cfg):
    idx = 0
    for node in cfg.nodes:
        print("node[" + str(idx) + "] => : ", end="")
        print("[" + node.lb_addr + ", " + node.ub_addr + "]: ", end="")
        print("dst: [" + ", ".join([str(dst) for dst in node.dsts])  + "]")
        idx+=1

def make_cfg():
    get_offset()
    
    gdb.execute('b main')
    gdb.execute('run')
    line = GDBMgr(gdb.execute('x/i $pc', to_string=True)[3:])
    create_breakpoints(line.addr)

    # gdb.execute('info breakpoints')

    # 初期化
    cfg = CFG()
    node = Node()
    # 最大到達アドレスは, デバッガのステップ実行で訪れたことのある最大のアドレス
    ub_addr = GDBMgr(gdb.execute('x/i $pc', to_string=True)[3:]).addr
    stack = []
    last_line = GDBMgr("0x0 :     test    code")

    while True:
        # print_nodes(cfg)
        # ステップ実行
        last_line = GDBMgr(gdb.execute('x/i $pc', to_string=True)[3:])
        gdb.execute('n')

        # 現在の行から2行分だけ逆アセンブルしたコードを取得して, 
        # その時のレジスタの値を保持
        # => 0x55555555463e <main+4>:     sub    rsp,0x10
        lines = gdb.execute('x/2i $pc', to_string=True).split('\n')
        lines[0] = lines[0][3:]  # delete =>
        lines = [GDBMgr(line) for line in lines if len(line) > 0]
        # print("lines: ", lines[0].opcode)
        lines[0].regs = get_registers()

        # 今いるノードのlb_addrを更新
        if int(lines[0].addr, 0) < int(node.lb_addr, 0):
            node.lb_addr = lines[0].addr
        
        # 1つ前のアドレスがjmp系命令だった時, 
        # 最大到達アドレスを更新
        # TODO: おかしい気がする
        if "j" in last_line.opcode:
            node.lb_addr = lines[0].addr
            cfg.append(node)
            cfg.append_dst_node(last_line.addr, lines[0].addr)

        # 次のオペコードがret命令だった時, 
        # ノードのub_addrとしてcfgのnodesに保存
        if 'ret' == lines[1].opcode:
            node.ub_addr = lines[1].addr
            cfg.append(node)

            # まだやり残したアドレスがある場合は,
            # 情報を復元して実施
            if len(stack) > 0:
                (restore, status) = stack.pop()
                restore_registers(restore.regs)
                # statusを逆転
                update_eflags(restore.opcode, not(status))
                # # print("restore: " + restore.raw)
                gdb.execute("j *" + restore.addr)
                continue
            break

        # 今の命令がjmp系命令の時
        if 'j' in lines[0].opcode:
            # Nodeの終端なので, ub_addrを埋める
            node.ub_addr = lines[0].addr
            # nodeをappend
            cfg.append(node)

            # trueに変更
            update_eflags(lines[0].opcode, True)

            # ジャンプ先の情報を取得
            gdb.execute("j *" + lines[0].addr)
            gdb.execute("n")
            line = GDBMgr(gdb.execute('x/i $pc', to_string=True)[3:])

            # 新たにノードを生成
            node = Node()
            node.lb_addr = line.addr
            cfg.append(node)

            # ジャンプ先に既に到達していた場合
            if int(line.addr, 0) < int(ub_addr, 0):
                # jmp命令の時はflagを書き換えても意味が無いのでそれ以上進まない

                # Trueの条件で実行したことにして, そのまま実行
                stack.append((lines[0], True))

                # ジャンプ先の情報を保存
                cfg.append_dst_node(lines[0].addr, line.addr)
                continue
            # ジャンプ先と最大到達アドレスが同じ場合
            elif int(line.addr, 0) == int(ub_addr, 0):
                # ジャンプ先の情報を保存
                cfg.append_dst_node(lines[0].addr, line.addr)

                # スタックに残っている情報を復元して, 
                # 以前実行したときと逆のフラグに書き換えて実行
                if len(stack) > 0:
                    (restore, status) = stack.pop()
                    restore_registers(restore.regs)
                    update_eflags(restore.opcode, not(status))
                    gdb.execute("j *" + restore.addr)
                continue
            
            # 初めてそのアドレスに到達したとき
            # 最大到達アドレスを更新して, 過去のノードをappend
            ub_addr = line.addr
            cfg.append(node)

            # print_nodes(cfg)
            # 新たにノードを生成
            node = Node()
            node.lb_addr = ub_addr
            cfg.append_dst_node(lines[0].addr, line.addr)

            # メモリをrestoreしてtopの情報を復元し, falseで実行 
            # print("regs: ", lines[0].regs)   
            restore_registers(lines[0].regs)
            update_eflags(lines[0].opcode, False)
            stack.append((lines[0], False))
            gdb.execute("j *" + lines[0].addr)
        else:
            # 次が区切れめなら, nodeを断ち切る
            if lines[1].addr == ub_addr:
                node.ub_addr = lines[0].addr
                cfg.append(node)
                cfg.append_dst_node(lines[0].addr, lines[1].addr)
                node = Node()
                node.lb_addr = lines[1].addr
                continue
    print_nodes(cfg)
    gdb.execute('quit')

make_cfg()
