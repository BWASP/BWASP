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
        try:
            requests.post(
                url="http://localhost:20102/api/job",
                headers={"accept": "application/json", "Content-Type": "application/json"},
                data=[{"targetURL": reqJsonData["target"]["url"], "knownInfo": reqJsonData["info"], "recursiveLevel": int(reqJsonData["tool"]["analysisLevel"]),
                       "uriPath": reqJsonData["target"]["path"]}]
            )
        except:
            abort(500)

        AutomatedAnalysis(reqJsonData["target"]["url"], reqJsonData["tool"]["analysisLevel"], reqJsonData)
    return render_template('automation/options.html', Title="Option for Automated analysis - BWASP")
