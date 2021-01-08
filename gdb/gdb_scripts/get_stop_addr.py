import gdb

def get_stop_addr_gdb():
    gdb.execute("set logging file tmp.out")
    gdb.execute('b main') # generate breakpoint
    gdb.execute('run')    # run until breakpoint(main)
    gdb.execute('set logging on')
    gdb.execute('x/i $pc')
    gdb.execute('set logging off')
    gdb.execute('quit')

    
get_stop_addr_gdb()
