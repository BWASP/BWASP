from flask import (
    Flask, g
)
from apis import blueprint as api
from models.CVE import cve_db as CVE_DB_Obj
from models.BWASP import bwasp_db as BWASP_DB_Obj
from werkzeug.middleware.proxy_fix import ProxyFix
import os

from flask_cors import CORS

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
CORS(app, resource={r'/api/*': {"Access-Control-Allow-Origin": "*"}})
CORS(app, resource={r'/api/*': {"Access-Control-Allow-Credentials": True}})

# config initialization
# from configs import DevelopmentsConfig, ProductionConfig
# config = DevelopmentsConfig()
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
app.config["SECRET_KEY"] = os.urandom(16)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///databases/BWASP.db"
app.config["SQLALCHEMY_BINDS"] = {
    "BWASP": f'sqlite:///{os.path.join(BASE_PATH, "databases/BWASP.db")}',
    "CVE": f'sqlite:///{os.path.join(BASE_PATH, "databases/CVE.db")}'
}
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

BWASP_DB_Obj.init_app(app)
CVE_DB_Obj.init_app(app)
app.app_context().push()
app.register_blueprint(api)

@app.before_request
def before_request():
    BWASP_DB_Obj.app = app
    CVE_DB_Obj.app = app
    BWASP_DB_Obj.create_all()
    g.BWASP_DBObj = BWASP_DB_Obj.session
    g.CVE_DBObj = CVE_DB_Obj.session

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'database'):
        g.BWASP_DBObj.close()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=20102, debug=True)
