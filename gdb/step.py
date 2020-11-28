import gdb
import sys

filename='test32'
gdb.execute('file ' + filename)
b = gdb.execute('b main')
gdb.execute('run')

with open('out_{}.txt'.format(filename), 'w') as f:
    try:
        for i in range(100):
            out = gdb.execute('step', to_string=True)
            if out == 'The program is not being run.':
                break
            lb = out.find('RIP')
            LEN = out[lb:].find('R8')
            line = str(out[lb:lb+LEN])
            if '\tj' in line:
                words = line.split()
                if int(words[1][6:6+14], 0) > 0x7ffff7000000:
                    break
                f.write(" ".join(words[1:]) + "\n")
    except Exception as e:
        print(e)
    finally:
        f.close()

gdb.execute('quit')
