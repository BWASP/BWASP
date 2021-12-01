import json

from flask import (
    Blueprint, g, render_template_string, request
)
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from modules.manual import start

NAME = 'manual'
bp = Blueprint(NAME, __name__, url_prefix='/')


@bp.route('/', methods=['GET', 'POST'])
def DataReqRes():
    if request.method == 'POST':
        data = request.get_json()
        return_data = start(data)
        return return_data
    else:
        return "Success"
'''
        return render_template_string(f"""
            <!Doctype html>
            <html>
            <head>
            </head>
            <body>
                {return_data}
            </body>
            </html>
            """)

    return render_template_string(f"""
                <!Doctype html>
                <html>
                <head>
                </head>
                <body>
                </body>
                </html>
                """)
'''