from flask import (
    Blueprint, render_template
)

NAME = 'report'
bp = Blueprint(NAME, __name__, url_prefix='/report')


@bp.route('/export')
def bpExport():
    return render_template('common/export.html', Title="Export report - BWASP")


@bp.route('/attack_vector')
def attack_Vector():
    return render_template('report/AttackVector.html', Title="Attack Vectors - BWASP")


@bp.route('/sub_domain')
def sub_Domain():
    return render_template('report/SubDomain.html', Title="Sub Domains - BWASP")
