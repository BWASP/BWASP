#! BWASP/bin/pytho

import os, sys
import webbrowser
import subprocess

if __name__ == "__main__":
    try:
        webbrowser.open("http://localhost:20102")
        webbrowser.open("http://localhost:20002")
        app = subprocess.Popen([sys.executable, "Web/app.py"])
        subprocess.call(["python", "RestAPI/app.py"])
    except KeyboardInterrupt:
        app.terminate()
        app2.terminate()