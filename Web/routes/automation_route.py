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

        data = [{"targetURL": reqJsonData['target'],
                 "knownInfo": json.dumps(reqJsonData['info']),
                 "recursiveLevel": reqJsonData['tool']['analysisLevel'],
                 "done": 0,
                 "maximumProcess": reqJsonData['maximumProcess']
                 }]

        try:
            requests.post(
                url="http://localhost:20102/api/job",
                headers={"accept": "application/json", "Content-Type": "application/json"},
                data=json.dumps(data)
            )
        except:
            abort(500, "Automation option setting data request error")

        AutomatedAnalysis(reqJsonData["target"]["url"], reqJsonData["tool"]["analysisLevel"], reqJsonData)

    return render_template('automation/options.html', Title="Option for Automated analysis - BWASP")
