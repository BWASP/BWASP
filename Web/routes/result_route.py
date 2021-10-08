from flask import (
    Blueprint, render_template, g
)

NAME = 'result'
bp = Blueprint(NAME, __name__, url_prefix='/')


@bp.route('/')
@bp.route('/start')
def mode_selection():
    return render_template('common/mode_selection.html', Title="Select analysis mode - BWASP")


@bp.route('/index')
def index():
    return render_template('index.html', Title="홈 - BWASP", data1=10, data2=60, data3=20)
