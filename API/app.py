from flask import (
    Flask, g
)
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS
import os
from models.BWASP import BWASP_DB
from models.CVE import CVE_DB


def create_app(config=None):
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    CORS(app, resource={r'/api/*': {"Access-Control-Allow-Origin": "*"}})
    CORS(app, resource={r'/api/*': {"Access-Control-Allow-Credentials": True}})

    # Config initialization
    from configs import DevelopmentsConfig, ProductionConfig
    if app.config['DEBUG']:
        config = DevelopmentsConfig()
    else:
        config = ProductionConfig()

    app.config.from_object(config)

    # API route initialization.
    from apis import blueprint as api
    app.register_blueprint(api)

    # App context initialization
    app.app_context().push()

    # Database initialization
    BWASP_DB.init_app(app)
    CVE_DB.init_app(app)
    BWASP_DB.app = app
    CVE_DB.app = app

    # Database create
    BWASP_DB.create_all()

    @app.before_request
    def before_request():
        # g object session initialization
        g.BWASP_DBObj = BWASP_DB.session
        g.CVE_DBObj = CVE_DB.session

    @app.teardown_request
    def teardown_request(exception):
        if hasattr(g, 'database'):
            g.BWASP_DBObj.close()

    return app


if __name__ == '__main__':
    application = create_app()
    application.run(host="0.0.0.0", port=20102, debug=True)
