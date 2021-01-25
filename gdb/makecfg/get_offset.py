import subprocess

get_offset_file_path = './gdb_scripts/get_offset.py'

def get_offset(target_file_path):
    init_args = ['rm', '-f', 'offset']
    subprocess.call(init_args)

    gdb_args = ['gdb', '-q', '-x', get_offset_file_path, target_file_path]
    subprocess.call(gdb_args)

    offset = ''
    with open('offset', 'r') as f:
        offset = f.readline()
    return offset

