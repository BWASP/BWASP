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
        data = start(request.form["reqdata"])

        return render_template_string(f"""
            <!Doctype html>
            <html>
            <head>
            </head>
            <body>
                {data}
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
