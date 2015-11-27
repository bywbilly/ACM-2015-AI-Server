from io import StringIO
from queue import Queue
from threading import Thread
from subprocess import Popen, PIPE
from shutil import copyfileobj

class ChildProcess():
    def __init__(self, args):
        self.qmain = Queue()
        self.qthread = Queue()
        self.thread = Thread(target=self._message_thread)
        self.stdin = StringIO()
        self.stdout = StringIO()
        self.child = Popen(args, bufsize=0, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)

        self.thread.start()

    def _message_thread(self):
        while True:
            op = self.qmain.get()
            if op['command'] == 'exit':
                break

            elif op['command'] == 'send':
                content = op['content']
                self.child.stdin.write(content)
                self.child.stdin.flush()
                self.stdin.write(content)
                self.qthread.put('finish')

            elif op['command'] == 'recv':
                content = ''
                while not content.endswith('END\n'):
                    chunk = self.child.stdout.readline()
                    if not chunk:
                        break
                    content += chunk
                content = content[:-4]
                self.stdout.write(content)
                self.qthread.put(content)

            else:
                raise "unsupported command"

    def send(self, content):
        self.qmain.put({ 'command': 'send', 'content': content })
        self.qthread.get()

    def recv(self, timeout):
        self.qmain.put({ 'command': 'recv' })
        content = self.qthread.get(timeout=timeout)
        return content

    def exit(self):
        self.qmain.put({ 'command': 'exit' })
        self.child.kill()
        self.thread.join()

    def save_stdio(self, path_stdin, path_stdout, path_stderr):
        with open(path_stdin, 'w')  as fin,\
             open(path_stdout, 'w') as fout,\
             open(path_stderr, 'w') as ferr:
            fin.write(self.stdin.getvalue())
            fout.write(self.stdout.getvalue())
            copyfileobj(self.child.stderr, ferr)
