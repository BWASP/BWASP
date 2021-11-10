from flask import (
    Blueprint, g
)

NAME = 'crx'
bp = Blueprint(NAME, __name__, url_prefix='/crx')


@bp.route('')
def crx():
    pass


@bp.route('/Receive')
def Receive():
    return "Receive"


@bp.route('/Send')
def Send():
    return "Send"
