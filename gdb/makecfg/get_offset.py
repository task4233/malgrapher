import subprocess

get_offset_file_path = './gdb_scripts/get_offset.py'

def get_offset(target_file_path):
    gdb_args = ['gdb', '-q', '-x', get_offset_file_path, target_file_path]
    offset  = subprocess.check_output(gdb_args)
    return offset



