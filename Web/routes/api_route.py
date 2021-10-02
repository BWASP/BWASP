from flask import (
    Blueprint, render_template, g, jsonify
)

NAME = 'api'
bp = Blueprint(NAME, __name__, url_prefix='/api')


@bp.route('/')
@bp.route('/api')
def apiInvalidRequest():
    return jsonify({"success": False, "message": "잘못된 요청입니다."})

@bp.route('/job/enroll')
def apiJobEnroll():
    return jsonify({"success": True})
