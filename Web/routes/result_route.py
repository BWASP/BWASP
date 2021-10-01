from flask import (
    Blueprint, render_template, g
)

NAME = 'result'
bp = Blueprint(NAME, __name__, url_prefix='/')


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')


@bp.route('/start')
def mode_selection():
    return render_template('common/mode_selection.html')
