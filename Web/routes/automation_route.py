from flask import (
    Blueprint, render_template, g,
    request, url_for, redirect
)

NAME = 'automation'
bp = Blueprint(NAME, __name__, url_prefix='/automation')


@bp.route('/options', methods=['GET', 'POST'])
def manual_options():
    if request.method == 'POST':
        reqJsonData = request.form['reqJsonData']
        """
        {
          "tool": {
            "analysisLevel": "1340",
            "optionalJobs": [
              "portScan"
            ]
          },
          "info": {
            "framework": [
              {
                "name": "react",
                "version": "1.12"
              }
            ],
            "backend": [
              {
                "name": "django",
                "version": "hello.world"
              }
            ]
          },
          "target": {
            "url": "https://naver.com/",
            "path": [
              "/a/b",
              "/c/d"
            ]
          }
        }
        """
        redirect(url_for('index'))
    return render_template('automation/options.html', Title="Option for Automated analysis - BWASP")
