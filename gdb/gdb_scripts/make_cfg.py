import gdb
import sys, os

# from create_breakpoints.py
def create_breakpoints():
    """ tested in test/test_create_breakpoints.py
    """
    gdb.execute('starti')
    func_names = get_functions()
    gdb.execute("b main")
    addrs = []
    for func_name in func_names:
        addrs.extend(get_addr_with_func_name(func_name))
    for addr in addrs:
        gdb.execute('b *' + addr)
    with open('breakpoints', 'w') as f:
        for addr in addrs:
            f.writelines(addr + "\n")
    if os.environ['ENV'] == 'test':
        gdb.execute('quit')

def get_functions():
    res_functions = []
    functions = gdb.execute('info functions', to_string=True).split('\n')
    for func in functions:
        # 関係のない部分
        if not('0x' in func):
            continue

        fs = func.split(' ')
        res_name = ''
        for idx in range(len(fs)):
            if '0x' in fs[idx]:
                # 外部ライブラリの構造は見ない
                # TODO: 見るように変えても良い
                if '0xf7' in fs[idx]:
                    break
                # アドレスの次が関数名(次は何故か空文字)
                # @pltがある場合は消す
                res_name = fs[idx+2].replace('@plt', '')
                break
        if len(res_name) > 0:
            res_functions.append(res_name)
    return res_functions

def get_addr_with_func_name(func_name):
    res_addrs = []
    order = ('disas \'%s\'' % func_name) if '.' in func_name else 'disas ' + func_name
    addrs = gdb.execute(order, to_string=True).split('\n')
    for addr in addrs:
        # 関係のない部分
        if not('0x' in addr):
            continue
        addr_r = addr.strip(' ').split(' ')
        res_addr = ''
        for ad in addr_r:
            if '0x' in ad:
                res_addr = ad
                break
        if len(res_addr) > 0:
            res_addrs.append(res_addr)
    return res_addrs

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
    create_breakpoints()
    
    gdb.execute('info breakpoints')

    gdb.execute('c')

    # 初期化
    cfg = CFG()
    node = Node()
    # 最大到達アドレスは, デバッガのステップ実行で訪れたことのある最大のアドレス
    ub_addr = GDBMgr(gdb.execute('x/i $pc', to_string=True)[3:]).addr
    stack = []
    last_line = GDBMgr("0x0 :     test    code")

    while True:
        print_nodes(cfg)
        # ステップ実行
        last_line = GDBMgr(gdb.execute('x/i $pc', to_string=True)[3:])
        gdb.execute('c')

        # 現在の行から2行分だけ逆アセンブルしたコードを取得して, 
        # その時のレジスタの値を保持
        # => 0x55555555463e <main+4>:     sub    rsp,0x10
        lines = gdb.execute('x/2i $pc', to_string=True).split('\n')
        lines[0] = lines[0][3:]  # delete =>
        lines = [GDBMgr(line) for line in lines if len(line) > 0]
        # print("lines: ", lines[0].opcode)
        lines[0].regs = get_registers()
        print(gdb.execute('x/10i $pc', to_string=True))

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

        # 次の命令がjmp系命令の時
        if 'j' in lines[1].opcode:
            # Nodeの終端なので, ub_addrを埋める
            node.ub_addr = lines[1].addr
            # nodeをappend
            cfg.append(node)

            # Falseの時の条件を保存
            next_line = lines[2].addr
            stack.append((lines[1], False))
            gdb.execute("j *" + lines[1].addr)


            # trueに変更
            update_eflags(lines[1].opcode, True)

            # ジャンプ先の情報を取得
            gdb.execute("j *" + lines[1].addr)
            gdb.execute("c")
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
