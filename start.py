#! BWASP/bin/python

import os, sys
import webbrowser
import subprocess

if __name__ == '__main__':
    try:
        webbrowser.open("http://localhost:20102")
        webbrowser.open("http://localhost:5000")
        app = subprocess.Popen([sys.executable, "Web/app.py"])
        subprocess.call(["python", "API/app.py"])
    except KeyboardInterrupt:
        app.terminate()