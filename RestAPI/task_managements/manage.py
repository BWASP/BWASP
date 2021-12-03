from flask import (
    Blueprint,
    abort,
    request,
    g,
    current_app as app
)
from models.model_returnObj import bwasp_db
import os
from configs import BASE_PATH

NAME = 'task'
bp = Blueprint(
    NAME,
    __name__,
    url_prefix='/task'
)


def database_init():
    # Database create
    from models.CSPEVALUATOR import CSPEVALUATOR_DB
    from models.PORTS import ports
    from models.PACKET import packet
    from models.SYSTEMINFO import systeminfo
    from models.JOB import job
    from models.DOMAIN import domain

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

        return f'{app.config["SQLALCHEMY_BINDS"], bwasp_db}'

    return app.config["SQLALCHEMY_DATABASE_URI"]
