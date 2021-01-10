import gdb

def create_breakpoint():
    addrs = []
    with open('breakpoint_addrs.dat', 'r') as f:
        addrs = f.readlines()
    print(addrs)
    gdb.execute("set logging file tmp.out")
    for addr in addrs:
        gdb.execute('b *' + addr)
    gdb.execute('set logging on')
    gdb.execute('info breakpoints')
    gdb.execute('set logging off')
    gdb.execute('quit')

create_breakpoint()