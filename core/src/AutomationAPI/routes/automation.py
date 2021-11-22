from flask import (
    Blueprint, render_template_string, request, abort
)
import sys, os, json, requests

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from Crawling.scouter import start

NAME = 'automation'
bp = Blueprint(NAME, __name__, url_prefix='/')


@bp.route('/', methods=['GET', 'POST'])
def DataReqRes():
    if request.method == 'POST':
        reqJsonData = request.get_json()
        print("@@@@@@@@@@@@@@@@@@@", reqJsonData)

        data = [{"targetURL": reqJsonData['target']['url'],
                 "knownInfo": json.dumps(reqJsonData['info']),
                 "recursiveLevel": reqJsonData['tool']['analysisLevel'],
                 "uriPath": reqJsonData['target']['path'],
                 "done": 0,
                 "maximumProcess": "None"
                 }]

        try:
            requests.post(
                url="http://localhost:20102/api/job",
                headers={"accept": "application/json", "Content-Type": "application/json"},
                data=json.dumps(data)
            )
        except:
            abort(500, "Automation option setting data request error")

        start(reqJsonData["target"]["url"], reqJsonData["tool"]["analysisLevel"], reqJsonData)

    return render_template_string("The BoB Web Application Security Project")
