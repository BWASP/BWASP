from flask import (
    Blueprint, render_template, request, abort
)
import json, requests
from Web.app import AutomatedAnalysis

NAME = 'manual'
bp = Blueprint(NAME, __name__, url_prefix='/manual')


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

        ManualAnalysis(reqJsonData["target"]["url"], reqJsonData["tool"]["analysisLevel"], reqJsonData)

    return render_template('manual/options.html', Title="Option for Manual analysis - BWASP")
