from flask import (
    Blueprint, render_template, request, abort
)
import json, requests
from Web.app import AutomatedAnalysis

NAME = 'automation'
bp = Blueprint(NAME, __name__, url_prefix='/automation')


@bp.route('/options', methods=['GET', 'POST'])
def manual_options():
    if request.method == 'POST':
        reqJsonData = json.loads(request.form["reqJsonData"])

        data = [{"targetURL": reqJsonData['target']['url'],
                 "knownInfo": json.dumps(reqJsonData['info']),
                 "recursiveLevel": reqJsonData['tool']['analysisLevel'],
                 "uriPath": reqJsonData['target']['path']
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
