import gdb
import itertools

filename='./target/test'
breakpoints = []

class Breakpoint:
    def __init__(self, addr, op, status=False):
        self.addr = addr
        self.op = op
        self.status = status

    def true_eflag_status(self):
        if self.op=="je":
            return "1<<6"

    def __str__(self):
        return f'addr: {self.addr}, op: {self.op}, status: {self.status}'

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
        words = line.split()
        from_addr = words[1]
        op = words[3]
        arg = words[4:]
        bi = Breakpoint(from_addr, op)

    # プログラムを確実に終了させる
    gdb.execute('quit')
    return
    
def enum_jumps():
    gdb.execute('file ' + filename)

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
            break

        # j*となるオペコードがあったらアドレスを覚えておく
        if '\tj' in line:
            # format
            # => 0x555555554694 <main+90>:	je     0x5555555546a4 <main+106> 
            # lineを入れたらsplitして全てを管理してくれるクラスを作る           
            words = line.split()
            from_addr = words[1]
            op = words[3]
            arg = words[4:]
            bi = Breakpoint(from_addr, op)
            breakpoints.append(bi)
            
            print("fr addr: " + " ".join(words[1:]))

    print(f'breakpoints: ({len(breakpoints)})')
    for bp in breakpoints:
        print(str(bp))

    # プログラムを確実に終了させる
    gdb.execute('quit')
    return


if __name__ == "__main__":
    enum_jumps()

    out = gdb.execute('info breakpoints', to_string=True)
    print(out)

    # bit全探索
    for status in range(2 ** len(breakpoints)):
        exec_with_status(status)
    
