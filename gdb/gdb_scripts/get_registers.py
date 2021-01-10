import gdb
import os

def get_registers():
    """ get_registers get register at that time and return values
    """
    
    # commands for test
    isTest = (os.environ['ENV'] == 'test')
    if isTest:
        gdb.execute('b main')
        gdb.execute('run')

    gdb.execute("set logging file tmp_get_registers.out")
    gdb.execute('set logging on')
    gdb.execute('info registers')
    gdb.execute('set logging off')

    if isTest:
        gdb.execute('quit')


get_registers()