#! BWASP/bin/python

import os
from Web import create_app as app

if __name__ == '__main__':
    app().run(host='0.0.0.0', port=5000, debug=True)
