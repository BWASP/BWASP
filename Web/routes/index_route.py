from flask import (
    Blueprint, render_template, g
)
from Web.models.BWASP import attackVector, CSPEmulator, domain, packets

NAME = 'result'
bp = Blueprint(NAME, __name__, url_prefix='/')


@bp.route('/')
@bp.route('/start')
def mode_selection():
    return render_template('common/mode_selection.html', Title="Select analysis mode - BWASP")


@bp.route('/dashboard')
def index():
    # result = {}.query.all()
    return render_template('index.html', Title="홈 - BWASP",
                           area_Chart={
                               "All_Result": 183,
                               "Web_Information": 20,
                               "Vulnerability_Doubt": 40,
                               "Attack_Vector": 50,
                               "Related_CVE": 16
                           },
                           header_box={
                               "Received": 426,
                               "Average_first_response_time": "1 min",
                               "Average_response_time": "3 min",
                               "Resolution_within_SLA": "94%"
                           },
                           pie_chart={
                               "data1": 80,
                               "data2": 5,
                               "data3": 15,
                           }
                           )
