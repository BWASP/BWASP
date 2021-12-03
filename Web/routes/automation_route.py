from flask import (
    Blueprint, render_template, request, abort
)
import json, requests, sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from Crawling.scouter import start

NAME = 'automation'
bp = Blueprint(NAME, __name__, url_prefix='/automation')


def AutomatedAnalysis(url, depth, options):
    start(url, int(depth), options)


@bp.route('/options', methods=['GET', 'POST'])
def automation_options():
    if request.method == 'POST':
        reqJsonData = request.get_json()

        AutomatedAnalysis(reqJsonData["target"], str(reqJsonData["tool"]["analysisLevel"]), reqJsonData)

    return render_template('automation/options.html', Title="Option for Automated analysis - BWASP")
