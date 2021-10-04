from flask import (
    Blueprint, render_template, g
)

from app import db
# from Web.app import db
query = db.select()
attack_Data = ""

NAME = 'common'
bp = Blueprint(NAME, __name__, url_prefix='/common')


@bp.route('/export')
def bpExport():
    return render_template('common/export.html', Title="Export report - BWASP")


@bp.route('/AttackVector')
def attack_Vector():
    return render_template('common/AttackVector.html', Title="Attack vectors - BWASP", data=attack_Data)
