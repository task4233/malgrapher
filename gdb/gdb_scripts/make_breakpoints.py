import gdb
import os

def create_breakpoints():
    addrs = []
    with open('breakpoint_addrs.dat', 'r') as f:
        addrs = f.readlines()
    print(addrs)
    gdb.execute("set logging file tmp_create_breakpoints.out")
    for addr in addrs:
        gdb.execute('b *' + addr)
    gdb.execute('set logging on')
    gdb.execute('info breakpoints')
    gdb.execute('set logging off')

    if os.environ['ENV'] == 'test':
        gdb.execute('quit')

create_breakpoints()