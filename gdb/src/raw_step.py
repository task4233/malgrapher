import gdb

filename='test'

gdb.execute('set debug target 1')
gdb.execute('file ' + filename)
b = gdb.execute('b main')
gdb.execute('run')

addrs_stk = []
is_end = False

# 出力先のファイルを指定する
with open('out_{}.txt'.format(filename), 'w') as f:
    # すべての経路を探索するまでループ
    while True:
        # next命令を実行
        out = gdb.execute('next', to_string=True)
        lb = out.find('=> ')
        LEN = out[lb:].find('\n')
        line = str(out[lb:lb+LEN])
        print("line => " + line)

        # 64bitならleave命令のときに終了する
        # 32bitならret命令の前に終了する
        if 'leave' in line:
            print('leave here')
            is_end = True
            if len(addrs_stk) == 0:
                break
            # スタックに載せているアドレス等を取り出す
            [inst, top_addr] = addrs_stk.pop()
            # 取り出したアドレスにブレークポイントを立てる
            b = gdb.execute('b *' + top_addr)
            if inst == 'je':
                # ZFを1にする
                gdb.execute('set $eflags |= (1 << 6)')
            # 取り出したアドレスにジャンプする
            out = gdb.execute('jump *' + top_addr)
            print('hasn\'t left yet')
            # ログを書く
            f.write('jump =>' + top_addr + '\n')
            continue

        # j*となるオペコードがあったときにそのアドレスを覚えておく
        if '\tj' in line:
            words = line.split()
            addr_fr_hex = words[1]
            print("fr: " + addr_fr_hex)
            
            words = line.split()
            addr_to_hex = words[4]
            print("to: " + addr_to_hex)
            # アドレスがスタックに飛んでいる場合は無視する
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
