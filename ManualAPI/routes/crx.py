from flask import (
    Blueprint, g
)

NAME = 'crx'
bp = Blueprint(NAME, __name__, url_prefix='/crx')


@bp.route('/Send', methods=['GET', 'POST'])
def Receive():
    return "/crx/Send"


@bp.route('/Receive', methods=['GET', 'POST'])
def Receive():
    return "/crx/Receive"
