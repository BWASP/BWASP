from flask import (
    Blueprint, render_template, g,
    request, url_for, redirect, jsonify
)
from Web import AutomatedAnalysis
import json

NAME = 'automation'
bp = Blueprint(NAME, __name__, url_prefix='/automation')


@bp.route('/options', methods=['GET', 'POST'])
def manual_options():
    AutomatedAnalysis(reqJsonData["target"]["url"], reqJsonData["tool"]["analysisLevel"], reqJsonData)
    return render_template('automation/options.html', Title="Option for Automated analysis - BWASP")
