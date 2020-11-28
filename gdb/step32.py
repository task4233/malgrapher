import gdb

filename='test32'

gdb.execute('file ' + filename)
b = gdb.execute('b main')
gdb.execute('run')

with open('out_{}.txt'.format(filename), 'w') as f:
    try:
        while True:
            out = gdb.execute('step', to_string=True)
            if out == 'The program is not being run.':
                break
            lb = out.find('EIP')
            LEN = out[lb:].find('EFLAGS')
            line = str(out[lb:lb+LEN])
            if '\tj' in line:
                words = line.split()
                if int(words[1][6:6+10], 0) > 0xf7000000:
                    break
                f.write(" ".join(words[1:]) + "\n")
    except Exception as e:
        print(e)
    finally:
        f.close()

gdb.execute('quit')
