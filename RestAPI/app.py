from flask import (
    Flask, g
)
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS

from models.BWASP.model_returnObj import bwasp_db
from models.BWASP.model_returnObj import cve_db
from models.BWASP.model_returnObj import task_db


def create_app(config=None):
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    CORS(app, resource={r'/api/*': {"Access-Control-Allow-Origin": "*"}})
    CORS(app, resource={r'/api/*': {"Access-Control-Allow-Credentials": True}})

    # Config initialization
    from configs import Developments_config, Production_config
    app.config['DEBUG'] = False  # NOT TESTING is False or TESTING is True
    if app.config['DEBUG']:
        config = Developments_config()
    else:
        config = Production_config()

    app.config.from_object(config)

    # Register routing for blueprint
    from apis import bp as api
    app.register_blueprint(api)

    # App context initialization
    app.app_context().push()

    # DB initialize and migrate
    cve_db.init_app(app)
    cve_db.app = app

    task_db.init_app(app)
    task_db.app = app

    bwasp_db.init_app(app)
    bwasp_db.app = app

    task_db.create_all(bind='TASK_MANAGER')

    if app.config['DEBUG']:
        # Database create
        from models.BWASP.CSPEVALUATOR import CSPEVALUATOR_DB
        from models.BWASP.PORTS import ports
        from models.BWASP.PACKET import packet
        from models.BWASP.SYSTEMINFO import systeminfo
        from models.BWASP.JOB import job
        from models.BWASP.DOMAIN import domain

        bwasp_db.create_all(bind='BWASP')

    @app.before_request
    def before_request():
        g.bwasp_db_obj = bwasp_db.session
        g.cve_db_obj = cve_db.session
        g.task_db_obj = task_db.session

    @app.teardown_request
    def teardown_request(exception):
        if hasattr(g, 'bwasp_db_obj'):
            g.bwasp_db_obj.close()

        if hasattr(g, 'cve_db_obj'):
            g.cve_db_obj.close()

        if hasattr(g, 'task_db_obj'):
            g.task_db_obj.close()

    return app


if __name__ == '__main__':
    application = create_app()
    application.run(host="0.0.0.0", port=20102, debug=True)
