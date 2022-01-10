import subprocess
import time
import threading

class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None
    
    def run(self, timeout):
        def target():
            self.process = subprocess.Popen(self.cmd, shell=True)
            self.process.communicate()
        
        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            self.process.terminate()
            print(f'{self.cmd} timeouted!')
            thread.join()


def generate_dot_by_radare2(bin_file_path: str, sample_name: str) -> str:
    """
    invokes radare2 command to generate dot file of CFG(Control Flow Graph)
    returns saved path of the dot file
    """

    if bin_file_path == '':
        raise ValueError('target bin_file_path must not be empty')
    if sample_name == '':
        raise ValueError('sample_name must not be empty')

    saved_file_path = f'out/{sample_name}.dot'

    # TODO: ファイル作成時にバグるので，とりあえずコメントアウトしておく Issue#24
    # # create file
    # with open(saved_file_path, 'w'): pass
    
    # args = ['r2', '-d', '-c', 'aa', '-c', f'agCd>{saved_file_path}', '-q', bin_file_path]
    # print(args)
    # try:        
    #     cmd = Command(args)
    #     cmd.run(timeout=1000)
    # except Exception as e:
    #     raise e
    
    return saved_file_path
