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
    return render_template('common/export.html', Title="보고서 내보내기 - BWASP")


@bp.route('/AttackVector')
def attack_Vector():
    return render_template('common/AttackVector.html', Title="공격 벡터 - BWASP", data=attack_Data)
