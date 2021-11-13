import re
from flask import (
    Blueprint, g, request
)
from modules import manual

NAME = 'crx'
bp = Blueprint(NAME, __name__, url_prefix='/crx')


@bp.route('/Send', methods=['GET', 'POST'])
def Send():
    if request.method == "GET":
        return manual.start(data)

    return "/crx/Send"


@bp.route('/Receive', methods=['GET', 'POST'])
def Receive():
    return "/crx/Receive"
