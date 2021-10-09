#! BWASP/bin/python

import os
import webbrowser
from Web import create_app as app

if __name__ == '__main__':
    webbrowser.open("http://localhost:5000")
    app().run(host='0.0.0.0', port=5000, debug=True)