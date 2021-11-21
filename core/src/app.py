import os, sys
import subprocess

if __name__ == '__main__':
    try:
        app = subprocess.Popen([sys.executable, "ManualAPI/app.py"])
        subprocess.call(["python", "AutomationAPI/app.py"])
    except KeyboardInterrupt:
        app.terminate()