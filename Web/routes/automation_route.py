from flask import (
    Blueprint, render_template, request, abort
)
from Web.app import AutomatedAnalysis
import json, requests

NAME = 'automation'
bp = Blueprint(NAME, __name__, url_prefix='/automation')


@bp.route('/options', methods=['GET', 'POST'])
def manual_options():
    if request.method == 'POST':
        reqJsonData = json.loads(request.form["reqJsonData"])

        data = [{"targetURL": f"{reqJsonData['target']['url']}",
                 "knownInfo": f"{reqJsonData['info']}",
                 "recursiveLevel": f"{int(reqJsonData['tool']['analysisLevel'])}",
                 "uriPath": f"{reqJsonData['target']['path']}"}]

        requests.post(
            url="http://localhost:20102/api/job",
            headers={"accept": "application/json", "Content-Type": "application/json"},
            data=str(data)
        )

        AutomatedAnalysis(reqJsonData["target"]["url"], reqJsonData["tool"]["analysisLevel"], reqJsonData)
    return render_template('automation/options.html', Title="Option for Automated analysis - BWASP")
