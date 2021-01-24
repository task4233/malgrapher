import gdb

gdb.execute('starti')
addrs = gdb.execute('disas _init', to_string=True).split('\n')
print(addrs[1].strip(' ').split(' ')[0])

