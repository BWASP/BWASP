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
        """
        {"tool":{"analysisLevel":"1","optionalJobs":[]},"info":{"server":[],"framework":[],"backend":[]},"target":{"url":"http://logos.sch.ac.kr","path":[""]}}
        """

        try:
            start(reqJsonData["target"]["url"], int(reqJsonData["tool"]["analysisLevel"]), reqJsonData)
            return render_template_string("Done"), 200
        except:
            return abort(500, f"Automation Analysis Exception error; Your options: {reqJsonData}")

    return render_template_string("The BoB Web Application Security Project")
