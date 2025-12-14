from flask import (
    Blueprint, render_template
)

NAME = 'result'
bp = Blueprint(NAME, __name__, url_prefix='/')


@bp.route('/')
@bp.route('/start')
def mode_selection():
    return render_template('common/mode_selection.html', Title="Select analysis mode - BWASP")


@bp.route('/dashboard')
def index():
    return render_template('index.html', Title="Home - BWASP")
