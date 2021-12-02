from flask import (
    Blueprint,
    abort,
    request,
    g,
    current_app as app
)
from models.BWASP import bwasp_db
import os
from configs import BASE_PATH

# BASE_PATH = os.path.dirname(os.path.abspath(__file__))

NAME = 'task'
bp = Blueprint(
    NAME,
    __name__,
    url_prefix='/task'
)


def database_init():
    # Database create
    bwasp_db.create_all(bind='BWASP')


@bp.route('/create', methods=['GET', 'POST'])
def manage():
    if request.method == "POST":
        values_idx_list = list()

        for values_idx in request.get_json().values():
            values_idx_list.append(values_idx)

        app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{os.path.join(BASE_PATH, "databases/" + values_idx_list[0] + ".db")}'
        app.config["SQLALCHEMY_BINDS"]['BWASP'] = f'sqlite:///{os.path.join(BASE_PATH, "databases/" + values_idx_list[0] + ".db")}'

        database_init()

        return f'{app.config["SQLALCHEMY_BINDS"] }'

    return app.config["SQLALCHEMY_DATABASE_URI"]
