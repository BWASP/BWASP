from flask import (
    Blueprint,
    abort,
    request,
    g,
    flash
)

from sqlalchemy import create_engine

NAME = 'task'
bp = Blueprint(
    NAME,
    __name__,
    url_prefix='/task'
)


class DatabaseOBJ:
    def __init__(self):
        self.engine = ""

    def engine(self):
        self.engine = create_engine('mysql+pymysql://scott:tiger@localhost/foo')


@bp.route('/manage', methods=['GET', 'POST'])
def manage():
    if request.method == "POST":
        return request.get_json()

    return "BWASP TASK MANAGER"


@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        return "POST"

    return "BWASP TASK MANAGER"
