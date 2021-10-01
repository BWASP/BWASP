from flask import (
    Blueprint, render_template, g
)

NAME = 'automation'
bp = Blueprint(NAME, __name__, url_prefix='/automation')


@bp.route('/options')
def manual_options():
    return render_template('automation/options.html', Title="자동 분석 옵션 설정 - BWASP")
