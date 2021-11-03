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
        AutomatedAnalysis(reqJsonData["target"]["url"], int(reqJsonData["tool"]["analysisLevel"]), reqJsonData["tool"]["optionalJobs"])

        response = requests.post(
            url="http://localhost:20102/api/job",
            headers={"accept": "application/json", "Content-Type": "application/json"},
            data={"targetURL": reqJsonData["target"]["url"], "knownInfo": reqJsonData["info"], "recursiveLevel": int(reqJsonData["tool"]["analysisLevel"]),
                  "uriPath": reqJsonData["target"]["path"]}
        )
        print(response.status_code)

    return render_template('automation/options.html', Title="Option for Automated analysis - BWASP")


"""
def AutomatedAnalysis(url, depth, options):
    start(url, int(depth), options)

reqJsonData: 
{
  "tool": {
    "analysisLevel": "1",
    "optionalJobs": []
  },
  "info": {
    "server": [],
    "framework": [],
    "backend": []
  },
  "target": {
    "url": "http://testphp.vulnweb.com/",
    "path": [
      ""
    ]
  }
}
"""
