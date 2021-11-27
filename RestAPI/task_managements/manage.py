from flask import (
    Blueprint,
    abort,
    request,
    g,
    current_app as app
)
from app import db
from sqlalchemy import create_engine

NAME = 'task'
bp = Blueprint(
    NAME,
    __name__,
    url_prefix='/task'
)


class DatabaseOBJ:
    def __init__(self):
        pass

    def engine(self, database_name):
        app.config["SQLALCHEMY_BINDS"][database_name] = f"mysql+pymysql://root:BWASPENGINE1234@bwasp-database-1/{database_name}?charset=utf8"
        return app.config["SQLALCHEMY_BINDS"]


data_access_object_of_db = DatabaseOBJ()


@bp.route('/manage', methods=['GET', 'POST'])
def manage():
    if request.method == "POST":
        return data_access_object_of_db.engine(request.get_json()["time"])

    return "BWASP TASK MANAGER"


@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        return "POST"

    return "BWASP TASK MANAGER"
