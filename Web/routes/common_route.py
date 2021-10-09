from flask import (
    Blueprint, render_template, g
)
from Web.models.BWASP import attackVector, CSPEmulator, domain, packets
import json

NAME = 'common'
bp = Blueprint(NAME, __name__, url_prefix='/common')


@bp.route('/export')
def bpExport():
    return render_template('common/export.html', Title="Export report - BWASP")


@bp.route('/attack_vector')
def attack_Vector():
    return render_template('common/AttackVector.html', Title="Attack vectors - BWASP", data=1)
