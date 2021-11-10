from flask import (
    Blueprint, g
)

NAME = 'manual'
bp = Blueprint(NAME, __name__, url_prefix='/manual')


@bp.route('/Receive', methods=['GET', 'POST'])
def Receive():
    return "/manual/Receive"


@bp.route('/Send', methods=['GET', 'POST'])
def Send():
    return "/manual/Send"
