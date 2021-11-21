from flask import (
    Blueprint, request, render_template_string
)
import sys, os, json

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from modules.manual import start

NAME = 'manual'
bp = Blueprint(NAME, __name__, url_prefix='/')


@bp.route('/', methods=['GET', 'POST'])
def DataReqRes():
    if request.method == 'POST':
        return_data = start(request.get_json())

        return return_data
    return render_template_string("The BoB Web Application Security Project")
