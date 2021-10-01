from flask import (
    Blueprint, render_template, g
)

from Web.app import db
query = db.select()
attack_Data = ""

NAME = 'common'
bp = Blueprint(NAME, __name__, url_prefix='/common')


@bp.route('/export')
def bpExport():
    return render_template('common/export.html')


@bp.route('/AttackVector')
def attack_Vector():
    return render_template('common/AttackVector.html', data=attack_Data)
