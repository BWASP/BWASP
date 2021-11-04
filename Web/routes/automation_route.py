from flask import (
    Blueprint, render_template, request
)
from Web.app import AutomatedAnalysis
import json, requests

NAME = 'automation'
bp = Blueprint(NAME, __name__, url_prefix='/automation')


@bp.route('/options', methods=['GET', 'POST'])
def manual_options():
    if request.method == 'POST':
        reqJsonData = json.loads(request.form["reqJsonData"])
        AutomatedAnalysis(reqJsonData["target"]["url"], reqJsonData["tool"]["analysisLevel"], reqJsonData)

        try:
            requests.post(
                url="http://localhost:20102/api/job",
                headers={"accept": "application/json", "Content-Type": "application/json"},
                data=json.dumps({"targetURL": reqJsonData["target"]["url"], "knownInfo": reqJsonData["info"], "recursiveLevel": int(reqJsonData["tool"]["analysisLevel"]),
                                 "uriPath": reqJsonData["target"]["path"]})
            )
        except:
            exit(1)

    return render_template('automation/options.html', Title="Option for Automated analysis - BWASP")
