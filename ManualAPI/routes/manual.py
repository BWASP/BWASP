from flask import (
    Blueprint, g
)

NAME = 'manual'
bp = Blueprint(NAME, __name__, url_prefix='/manual')


@bp.route('')
def manual():
    pass


@bp.route('/Receive')
def Receive():
    return "Receive"


@bp.route('/Send')
def Send():
    return "Send"


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
