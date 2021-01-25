import gdb
import os, sys

def create_breakpoints():
    gdb.execute('starti')
    func_names = get_functions()
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

create_breakpoints()