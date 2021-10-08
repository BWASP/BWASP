from flask import (
    Blueprint, render_template, g,
    request, url_for, redirect, jsonify
)
from Web.models.BWASP import job
from Web import AutomatedAnalysis
import json

NAME = 'automation'
bp = Blueprint(NAME, __name__, url_prefix='/automation')


@bp.route('/options', methods=['GET', 'POST'])
def manual_options():
    if request.method == 'POST':
        reqJsonData = json.loads(request.form['reqJsonData'])
        g.db.add(
            # targetURL, knownInfo, recursiveLevel, uriPath
            job(targetURL=str(reqJsonData["target"]["url"]), knownInfo=str(reqJsonData["info"]), recursiveLevel=str(reqJsonData["tool"]["analysisLevel"]), uriPath=str(reqJsonData["target"]["path"]))
        )
        g.db.commit()

        # AutomatedAnalysis(reqJsonData["target"]["url"], reqJsonData["tool"]["analysisLevel"], reqJsonData["tool"]["optionJobs"])

        return jsonify({"success": True})
    return render_template('automation/options.html', Title="Option for Automated analysis - BWASP")
