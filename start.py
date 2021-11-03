#! BWASP/bin/python

import os, sys
import webbrowser
import subprocess

if __name__ == '__main__':
    webbrowser.open("http://localhost:5000")
    webbrowser.open("http://localhost:20102")
    subprocess.call(["python", "Web/app.py"])
    subprocess.call(["python", "API/app.py"])
