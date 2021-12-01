#! BWASP/bin/python

import os, sys
import webbrowser
import subprocess
from multiprocessing import Process

def exec_server(name):
    app = subprocess.Popen([sys.executable, name])


if __name__ == '__main__':
    # try:
    proc_list = []
    namelist =["Web/app.py","API/app.py","ManualAPI/app.py"]
    webbrowser.open("http://localhost:20102")
    webbrowser.open("http://localhost:20002")
    for name in namelist:
        proc = Process(target=exec_server,args=(name,))
        proc.start()
        proc_list.append(proc)
