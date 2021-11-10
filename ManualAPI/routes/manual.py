from flask import (
    Blueprint, g
)

NAME = 'manual'
bp = Blueprint(NAME, __name__, url_prefix='/manual')


@bp.route('/Send', methods=['GET', 'POST'])
def Receive():
    return "/manual/Send"


@bp.route('/Receive', methods=['GET', 'POST'])
def Receive():
    return "/manual/Receive"


"""
[
  {
    "http://testphp.vulnweb.com/admin.php": {
      "SQL injection": {
        "type": []
      },
      "XSS": {
        "type": [],
        "header": {
          "HttpOnly": false,
          "X-Frame-Options": false
        }
      },
      "CORS": false,
      "Allow Method": [],
      "Open Redirect": "url",
      "s3": [],
      "jwt": [],
      "subdomain": [],
      "api_key": {
        "facebook": "asdf"
      }
    },
    "http://testphp.vulnweb.com/login.php": {
      "SQL injection": {
        "type": []
      },
      "XSS": {
        "type": [],
        "header": {
          "HttpOnly": false,
          "X-Frame-Options": false
        }
      },
      "CORS": false,
      "Allow Method": [],
      "Open Redirect": "url",
      "s3": [],
      "jwt": [],
      "subdomain": [],
      "api_key": {
        "facebook": "asdf"
      }
    }
  }
]
"""
