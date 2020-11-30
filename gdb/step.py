import gdb

filename='test32'

# gdb.execute('set debug target 1')
gdb.execute('file ' + filename)
b = gdb.execute('b main')
gdb.execute('run')

addrs_stk = []

with open('out_{}.txt'.format(filename), 'w') as f:
    while True:
        out = gdb.execute('next', to_string=True)
        lb = out.find('=> ')
        LEN = out[lb:].find('\n')
        line = str(out[lb:lb+LEN])
        print("line => " + line)

        if 'leave' in line:
            print('leave here')
            if len(addrs_stk) == 0:
                break
            [inst, top_addr] = addrs_stk.pop()
            b = gdb.execute('b *' + top_addr)
            if inst == 'je':
                # ZFを1にする
                gdb.execute('set $eflags |= (1 << 6)')
            out = gdb.execute('jump *' + top_addr)
            print('hasn\'t left yet')
            f.write('jump =>' + top_addr + '\n')
            continue
        
        if '\tj' in line:
            words = line.split()
            addr_fr_hex = words[1]
            print("fr: " + addr_fr_hex)
            
            words = line.split()
            addr_to_hex = words[4]
            print("to: " + addr_to_hex)
            if int(addr_to_hex, 0) > 0x7ffff7000000:
                break
            
            f.write(" ".join(words[1:]) + "\n")
            print("line: " + line)
            # ZF=0とZF=1の両方を探索する
            if words[3] == 'je':
                # ZF=0で探索(ZF=0にする)
                gdb.execute('set $eflags &= ~(1 << 6)')
                addrs_stk.append([words[3], addr_fr_hex])
                print("addrs_stk: ", end="")
                print(addrs_stk)
                f.write("\n")
            print(out)
            

gdb.execute('quit')
