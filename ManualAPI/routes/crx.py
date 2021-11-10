from flask import (
    Blueprint, g
)

NAME = 'crx'
bp = Blueprint(NAME, __name__, url_prefix='/crx')


@bp.route('/Receive', methods=['GET', 'POST'])
def Receive():
    return "/crx/Receive"


@bp.route('/Send', methods=['GET', 'POST'])
def Send():
    return "/crx/Send"