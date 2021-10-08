from flask import (
    Blueprint, render_template, g,
    request, url_for, redirect
)
from Web.models.BWASP import job

NAME = 'test'
bp = Blueprint(NAME, __name__, url_prefix='/test')


@bp.route('/')
def apiInvalidRequest():
    result = g.db.query(
        job
    ).all()
    # result = job.query.all()
    return str(result)
