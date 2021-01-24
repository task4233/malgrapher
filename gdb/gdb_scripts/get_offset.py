import gdb
import os

def get_offset():
	isTest = (os.environ['ENV'] == 'test')
	static=''
	lines = gdb.execute('info files', to_string=True).split('\n')
	for line in lines:
		if 'Entry' in line:
			static = line.split(' ')[2]
			break
	gdb.execute('starti')
	dynamic = ''
	lines = gdb.execute('info files', to_string=True).split('\n')
	for line in lines:
		if 'Entry' in line:
			dynamic = line.split(' ')[2]
			break
	offset = hex(int(dynamic, 0) - int(static, 0))
	if isTest:
		with open('offset', 'w') as f:
			f.write(offset)
		gdb.execute('quit')
	else:
		return offset

get_offset()