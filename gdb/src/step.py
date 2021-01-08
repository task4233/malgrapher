import gdb
import itertools

filename='./target/test'
breakpoints = []

class GdbCtx:
    def __init__(self, gdb):
        self.gdb = gdb
        self.gdb.execute('file ' + filename)
    
    def __del__(self):
        del self.gdb

class Breakpoint:
    def __init__(self, line):
        words = line.split()
        # format
        # => 0x555555554694 <main+90>:	je     0x5555555546a4 <main+106>
        from_addr = words[1]
        op = words[3]
        args = words[4:]
        self.from_addr = from_addr
        self.op = op
        self.args = args

    def update_carry_flag(self, status):
        return (1<<0) & status

    def update_zero_flag(self, status):
        return (1<<6) & status

    def update_sign_flag(self, status):
        return (1<<7) & status

    def true_eflag_status(self):
        if self.op=="je":
            return "1<<6"

def exec_with_status(status):
    gdb.execute('file ' + filename)

    # bit全探索用のbreakpoint作成
    for i in range(len(breakpoints)):
        if ((status >> i) & 1):
            gdb.execute('b *' + breakpoints[i].addr)
    gdb.execute('b main')

    while True:
        # breakpointまで飛ぶ
        out = gdb.execute('continue', to_string=True)
        lb = out.find('=> ')
        LEN = out[lb:].find('\n')
        line = str(out[lb:lb+LEN])
        # print("line => " + line)

        # leaveだったら抜ける
        if 'leave' in line:
            break
        
        # format
        # => 0x555555554694 <main+90>:	je     0x5555555546a4 <main+106>
        # breakpoint_information = Breakpoint(line)

    # プログラムを確実に終了させる
    gdb.execute('quit')
    return
    
def enum_jumps():
    idx = 0
    b = gdb.execute('b main')
    gdb.execute('run')
    
    while True:
        # 次の場所まで飛ぶ
        out = gdb.execute('next', to_string=True)
        lb = out.find('=> ')
        LEN = out[lb:].find('\n')
        line = str(out[lb:lb+LEN])
        # print("line => " + line)

        # leaveだったら抜ける
        if 'leave' in line:
            gdb.execute("set $eflags |= (1 << 6)")
            gdb.execute("j *" + breakpoints[idx].from_addr)
            idx+=1
            break

        # 最初はtrueの状態から読みだす
        # stackからpopされたときはfalseの条件に変える
        # j*となるオペコードがあったらアドレスを覚えておく
        if '\tj' in line:
            # format
            # => 0x555555554694 <main+90>:	je     0x5555555546a4 <main+106>
            breakpoint_information = Breakpoint(line)
            breakpoints.append(breakpoint_information)

            gdb.execute("b *" + breakpoint_information.from_addr)
            gdb.execute("set $eflags &= ~(1 << 6)")

            print("fr addr: " + " ".join(line.split()[1:]))

    print(f'breakpoints: ({len(breakpoints)})')
    for bp in breakpoints:
        print(str(bp))
    return


if __name__ == "__main__":
    gdbctx = GdbCtx(gdb)

    enum_jumps()

    out = gdb.execute('info breakpoints', to_string=True)
    print("[INFO] breakpoints: ", out)

    # プログラムを 確実に終了させる
    gdb.execute('quit')

    # bit全探索
    """ for status in range(2 ** len(breakpoints)):
        exec_with_status(status) """
