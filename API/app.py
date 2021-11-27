from flask import (
    Flask, g
)
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS
from models.BWASP import bwasp_db
from models.CVE import cve_db


def create_app(config=None):
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    CORS(app, resource={r'/api/*': {"Access-Control-Allow-Origin": "*"}})
    CORS(app, resource={r'/api/*': {"Access-Control-Allow-Credentials": True}})

    # Config initialization
    from configs import Developments_config, Production_config
    if app.config['DEBUG']:
        config = Developments_config()
    else:
        config = Production_config()

    app.config.from_object(config)

    # API route initialization.
    from apis import blueprint as api
    app.register_blueprint(api)

    # App context initialization
    app.app_context().push()

    # Database initialization
    bwasp_db.init_app(app)
    cve_db.init_app(app)
    bwasp_db.app = app
    cve_db.app = app

    # Database create
    bwasp_db.create_all()

    @app.before_request
    def before_request():
        # g object session initialization
        g.bwasp_db_obj = bwasp_db.session
        g.cve_db_obj = cve_db.session

    @app.teardown_request
    def teardown_request(exception):
        if hasattr(g, 'bwasp_db_obj'):
            g.bwasp_db_obj.close()

        if hasattr(g, 'cve_db_obj'):
            g.cve_db_obj.close()

    return app


if __name__ == '__main__':
    application = create_app()
    application.run(host="0.0.0.0", port=20102, debug=True)
