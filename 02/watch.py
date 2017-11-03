#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'wl'

import os, sys,time ,subprocess

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def log(s):
    print('[Monitor] %s' % s)

class MyFileSystemEventHander(FileSystemEventHandler):

    def __init__(self, fn):
        super(MyFileSystemEventHander, self).__init__()
        self.restart = fn

    def on_any_event(self, event):
        if event.src_path.endswith('.py'):
            log('Python source file changed: %s' % event.src_path)
            self.restart()

# 它只是一个装饰物，真正的命令是启动服务的命令
command = ['echo', 'ok']
process = None

def kill_process():
    global process
    if process:
        log('Kill process [%s]...' % process.pid)
        process.kill()
        process.wait()
        log('Process ended with code %s.' % process.returncode)
        process = None

def start_process():
    global process, command
    log('Start process %s...' % ' '.join(command))
    # 根据watch.py的启动命令，启动服务，并且得到process进程对象
    process = subprocess.Popen(command, stdin=sys.stdin, stdout=sys.stdout,
            stderr=sys.stderr)

def restart_process():
    global process
    log('Restart process  %d' % process.pid)
    kill_process()
    start_process()

def start_watch(path, callback):
    observer = Observer()
    # 当 path以及子目录下文件改变，则触发 restart_process 函数
    observer.schedule(MyFileSystemEventHander(restart_process), path,
            recursive=True)
    observer.start()
    log('Watching directory %s...' % path)
    start_process()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    argv = sys.argv[1:]
    if not argv:
        print('Usage: ./watch.py your-script.py')
        exit(0)
    if argv[0] != 'python3':
        argv.insert(0, 'python3')
    command = argv
    path = os.path.abspath('.')
    start_watch(path, None)
